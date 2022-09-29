from flask import Flask
from flask_restx import Api
from .config.config import config_dict
from .file_uploads.views import fuploads_namespace
from .utils import db
from .models.files import Files
from .models.columns import Columns

def create_app(config=config_dict['dev']):
    app=Flask(__name__)   

    app.config.from_object(config)

    db.init_app(app)

    api=Api(
        app,
        title='File Upload API',
        description=('REST API to upload files and'
                    ' return details about files'
                    ' uploaded to webserver')
    )

    api.add_namespace(fuploads_namespace)

    #Shell to access/create database
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'Files':Files,
            'Columns':Columns
        }

    return app

