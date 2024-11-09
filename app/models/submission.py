from app import db
from app.models.assignment import Assignment 
from app.models.user import User  

class Submission(db.Model):
    __tablename__ = 'submission'

    submission_id = db.Column(db.Integer, primary_key=True) 
    submission_score = db.Column(db.Float, nullable=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.assignment_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    submission_date = db.Column(db.String(10), nullable=False)
    submission_file = db.Column(db.String(300), nullable=False)
    submission_status = db.Column(db.String(15), nullable=False)
    comment_ai = db.Column(db.String(45), nullable=True)
    comment_professor = db.Column(db.String(45), nullable=True)

    assignment = db.relationship('Assignment', backref=db.backref('submissions', lazy=True))
    student = db.relationship('User', backref=db.backref('submissions', lazy=True))

    def __init__(self, submission_score, assignment_id, student_id, submission_file, submission_status, submission_date, comment_ai=None, comment_professor=None):
        self.submission_score = submission_score
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.submission_file = submission_file
        self.submission_status = submission_status
        self.submission_date = submission_date
        self.comment_ai = comment_ai
        self.comment_professor = comment_professor

    def __repr__(self):
        return f'<Submission {self.submission_id}>'