from app import db
from app.models.user import User
from app.models.course import Course

class Registration(db.Model):
    __tablename__ = 'registration'
    
    registration_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False) 
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'),nullable=False)  

    student = db.relationship('User', backref='registrations', lazy=True)
    course  = db.relationship('Course', backref='registrations', lazy=True)

    def __init__(self, student_id, course_id):
        self.student_id = student_id
        self.course_id = course_id

    def __repr__(self):
        return f'<Registration {self.registration_id}, Student {self.student_id}, Course {self.course_id}>'
