from app import db

class Ai_answer(db.Model):
    __tablename__ = 'ai_answer'

    answer_id = db.Column(db.Integer, primary_key=True) 
    answer = db.Column(db.String(100), unique=True, nullable=False) 

    def __init__(self, answer):
        self.answer = answer

    def __repr__(self):
        return f'<Ai_answer {self.answer_id}, Answer: {self.answer}>'
