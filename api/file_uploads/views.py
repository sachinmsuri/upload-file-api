from flask_restx import Namespace
from flask_restx import Resource
from flask_restx import reqparse
from flask_restx import abort
from flask_restx import fields
from werkzeug.datastructures import FileStorage
from flask import request
from flask import jsonify
from flask import make_response
import os
import uuid
from ..utils import db
from ..models.files import Files
from ..models.columns import Columns
import pandas as pd
from pandas.api.types import is_numeric_dtype

fuploads_namespace = Namespace(
    'files',
    description='Upload files and acess information\
                on previously stored files'
)

#Arguments for /upload POST request
upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', type=FileStorage, location='uploads')

@fuploads_namespace.route('/upload')
@fuploads_namespace.expect(upload_parser)
@fuploads_namespace.doc(
    description=("Upload a new file to web server. After the file "
                " has sucesfukly uploaded the FileID will be returned"
                " You are unable to upload a file if it is empty,"
                " only has headers or is not in a text/csv format.")
)
class Upload(Resource):

    def post(self):
        if not request.files:
            return {'message':'No file uploaded'}, 400

        file = request.files.getlist('file')[0]

        if file.content_type != 'text/csv':
            return {'message':'File needs to be of type text/csv'}, 400

        if file.seek(0, os.SEEK_END) == 0:
            return {'message':'Unable to upload empty file'}, 400
        
        #Generate UUID
        id = str(uuid.uuid1())

        #Save file to uploads folder
        file.stream.seek(0)
        file.save(
        f'uploads/{id}.csv'
        )

        df = pd.read_csv(f'uploads/{id}.csv', sep=",")
        
        #Do not save if file is empty / colums have no data
        if df.empty:
            return {'message':'Columns have no data'}, 400
        
        #Add file details to files table
        new_file = Files(
            fileid=id,
            size=file.seek(0, os.SEEK_END),
            type='text/csv'
        )

        db.session.add(new_file)
        db.session.commit()

        #Add columns and datatype to Columns table
        for column, type in df.dtypes.to_dict().items():
            new_column = Columns(
                fileid=id,
                name=column,
                datatype=str(type)
            )

            db.session.add(new_column)
            db.session.commit()

        return make_response(jsonify({'guid':id}), 201)

@fuploads_namespace.route('/file_info/<string:guid>')
@fuploads_namespace.doc(
    description=("Retreive information for a specifc file based on a FileID"
                " File Info: Column Names, No. of Rows, File Size"
                " and File Type ")
)
class FileInfo(Resource):
    def get(self, guid):
        file = Files.query.filter_by(fileid=guid).first()

        if file:
            columns_data = {}
            file = file.__dict__

            columns = Columns.query.filter_by(fileid=guid).all()
            for column in columns:
                columns_data[column.name] = column.datatype

            #Combine data from columns and files table into single dict
            file['columns'] = columns_data
            del file["_sa_instance_state"]

            return make_response(jsonify(file), 200)
        else:
            return {'message':'GUID does not exist'}, 404

@fuploads_namespace.route('/column_info/<string:guid>/<string:name>')
@fuploads_namespace.doc(
    description=("Return the median, min and max value for a specifc"
                "columns in a file")
)
class ColumnInfo(Resource):

    def get(self, guid, name):
        df = pd.read_csv(f'uploads/{guid}.csv')

        if name not in df.columns:
            return {'message':'Column does not exist'}, 404
        
        if not is_numeric_dtype(df[name]):
            return {'message':'Column does not contain numerical values'}, 200
        
        result = {
            'min': df[name].min(),
            'max': df[name].max(),
            'medium': df[name].median()
        }

        return make_response(jsonify(result), 200)
    



        

        


