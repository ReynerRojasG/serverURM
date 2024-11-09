from app import db
from app.models.course import Course  
from app.models.user import User  

class Assignment(db.Model):
    __tablename__ = 'assignment'

    assignment_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)  
    professor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  
    course_statement = db.Column(db.String(300), nullable=False)
    assignment_type = db.Column(db.String(12), nullable=False)
    initial_date = db.Column(db.String(10), nullable=False)
    final_date = db.Column(db.String(10), nullable=False)

    course = db.relationship('Course', backref='assignments', lazy=True)  
    professor = db.relationship('User', backref='assignments', lazy=True) 

    def __init__(self, course_id, professor_id, course_statement, assignment_type, initial_date, final_date):
        self.course_id = course_id
        self.professor_id = professor_id
        self.course_statement = course_statement
        self.assignment_type = assignment_type
        self.initial_date = initial_date
        self.final_date = final_date

    def __repr__(self):
        return f'<Assignment {self.assignment_id}, Type: {self.assignment_type}, Course: {self.course_id}>'
