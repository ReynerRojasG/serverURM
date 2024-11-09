#from app.models import db
from app import db 
from app.models.university import University  

class Faculty(db.Model):
    __tablename__ = 'faculty'
    
    faculty_id = db.Column(db.Integer, primary_key=True) 
    faculty_name = db.Column(db.String(45), unique=True, nullable=False)
    faculty_information = db.Column(db.String(45), unique=True, nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('university.university_id'), nullable=False)  
    
    university = db.relationship('University', backref='faculties', lazy=True)

    def __init__(self, faculty_name, faculty_information, university_id):
        self.faculty_name = faculty_name
        self.faculty_information = faculty_information
        self.university_id = university_id

    def __repr__(self):
        return f'<Faculty {self.faculty_id}, Name: {self.faculty_name}>'
