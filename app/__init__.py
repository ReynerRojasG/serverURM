from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    mi_aplication = Flask(__name__)
    mi_aplication.config['SECRET_KEY'] = 'supersecretkey'
    mi_aplication.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/avi'
    mi_aplication.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(mi_aplication)

    from app.controllers.user_controller import user_bp
    from app.controllers.university_controller import university_bp
    from app.controllers.faculty_controller import faculty_bp
    from app.controllers.department_controller import department_bp
    from app.controllers.course_controller import course_bp
    from app.controllers.assignment_controller import assignment_bp
    from app.controllers.submissions_controller import submission_bp
    from app.controllers.registration_controller import registration_bp
    from app.controllers.ai_answer_controller import ai_answer_bp

    mi_aplication.register_blueprint(user_bp, url_prefix='/users') 
    mi_aplication.register_blueprint(university_bp, url_prefix='/universities')
    mi_aplication.register_blueprint(faculty_bp, url_prefix='/faculties')
    mi_aplication.register_blueprint(department_bp, url_prefix='/department')
    mi_aplication.register_blueprint(course_bp, url_prefix='/course')
    mi_aplication.register_blueprint(assignment_bp, url_prefix='/assignments')
    mi_aplication.register_blueprint(submission_bp, url_prefix='/submission')
    mi_aplication.register_blueprint(registration_bp, url_prefix='/registration')
    mi_aplication.register_blueprint(ai_answer_bp, url_prefix='/answer')

    with mi_aplication.app_context():
        db.create_all()

    return mi_aplication
