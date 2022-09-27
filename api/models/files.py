from tokenize import String
from ..utils import db
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Files(db.Model):
    """Model to store all unique File GUID's, file type,
    file size and date for all files uploaded to web server.
    """
    __tablename__='files'
    fileid=db.Column(db.String(), primary_key=True)
    size=db.Column(db.Float())
    type=db.Column(db.String())
    date=db.Column(db.DateTime(), default=datetime.utcnow)
    
    def __repr__(self):
        return f'<GUID {self.id}>'
