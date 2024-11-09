from app import db 
from app.models.user import User  
from app.models.department import Department  

class Course(db.Model):
    __tablename__ = 'course'

    course_id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False) 
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'), nullable=False)  
    course_name = db.Column(db.String(45), unique=True, nullable=False)
    course_information = db.Column(db.String(45), nullable=False)

    professor = db.relationship('User', backref='courses', lazy=True) 
    department = db.relationship('Department', backref='courses', lazy=True)  

    def __init__(self, professor_id, department_id, course_name, course_information):
        self.professor_id = professor_id
        self.department_id = department_id
        self.course_name = course_name
        self.course_information = course_information

    def __repr__(self):
        return f'<Course {self.course_id}, Name: {self.course_name}>'
