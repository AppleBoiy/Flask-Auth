from app import db
from sqlalchemy_serializer import SerializerMixin


class Greet(db.Model, SerializerMixin):
    __tablename__ = "greetings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    msg = db.Column(db.String)
    
    def __init__(self, msg):
        self.msg = msg
