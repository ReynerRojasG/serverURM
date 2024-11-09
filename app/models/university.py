from app import db 
from app.models.user import User

class University(db.Model):
    __tablename__ = 'university'
    
    university_id = db.Column(db.Integer, primary_key=True)
    university_name = db.Column(db.String(45), unique=True, nullable=False)
    users = db.relationship('User', backref='university', lazy=True)

    def __init__(self, university_name):
        self.university_name = university_name

    def __repr__(self):
        return f'<University {self.university_id}>'
