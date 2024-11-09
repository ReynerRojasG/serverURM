from app import db 

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey('university.university_id'), nullable=True)
    user_name = db.Column(db.String(45), unique=True, nullable=False)
    user_type = db.Column(db.String(14), nullable=False)
    user_password = db.Column(db.String(10), nullable=False)
    user_identification = db.Column(db.String(10), nullable=False)

    def __init__(self, university_id, user_name, user_password, user_type, user_identification):
        self.university_id = university_id
        self.user_name = user_name
        self.user_password = user_password
        self.user_type = user_type
        self.user_identification = user_identification

    def __repr__(self):
        return f'<User {self.user_id}>'
