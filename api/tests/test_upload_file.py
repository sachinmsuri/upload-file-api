import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from flask import json
import os
import io

class FilesTestCase(unittest.TestCase):

    def setUp(self):
        """Create new instance of Flask App with an 
        in-memory database.
        """
        self.app = create_app(config=config_dict['test'])
        self.appctx=self.app.app_context()

        self.appctx.push()

        self.client=self.app.test_client()

        db.create_all()

    def tearDown(self):
        """Close instance of Flask App and drop
        all tables within the in-memory database.
        """
        db.drop_all()

        self.appctx.pop()

        self.app=None

        self.client=None
    
    def upload_file(self, name):
        """Helper function to upload file to webserver
        and file details to the files table.
        """
        file_upload = os.path.join(
            os.getcwd(), f'api/tests/test_files/{name}'
        )

        data = {
            'file':(open(file_upload, 'rb'), file_upload)
        }
       
        response=self.client.post(
            '/files/upload',
            data=data,
            content_type='multipart/form-data'
        )

        return response

    def test_upload_file(self):
        """Test if we are able to upload file details to the files
        table in database and store within uploads folder on webserver.
        """
        response = self.upload_file('test.csv')
        assert response.status_code == 201

    def test_file_info(self):
        """Test if we are able to query a file and find details
        about a column
        """
        file = json.loads(self.upload_file('test.csv').data)
        rfile_info = self.client.get(
             f"files/file_info/{file['guid']}"
        )
        rcol_info = self.client.get(
            f"files/column_info/{file['guid']}/Distance"
        )
        
        assert rfile_info.status_code == 200
        assert rcol_info.status_code == 200

    def test_empty_file(self):
        response = self.upload_file('empty_test.csv')
        assert response.status == '400 BAD REQUEST'