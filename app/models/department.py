from app import db 

class Department(db.Model):
    __tablename__ = 'department'
    department_id = db.Column(db.Integer, primary_key=True) 
    department_name = db.Column(db.String(45), unique=True, nullable=False)
    department_information = db.Column(db.String(45), unique=True, nullable=False)
    faculty_id = db.Column(db.Integer, nullable = False)
    
    def __repr__(self):
        return f'<Department {self.id}>'