from ..utils import db

class Columns(db.Model):
    """Model to store all columns and colum datatype
    for all files uploaded to webserver
    """
    __tablename__='columns'
    id = db.Column(db.Integer, primary_key=True)
    fileid=db.Column(db.String(), db.ForeignKey('files.fileid'))
    name=db.Column(db.String())
    datatype=db.Column(db.String())
    
    def __repr__(self):
        return f'<GUID {self.id}>'
