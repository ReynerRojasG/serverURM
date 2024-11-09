from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/avi'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    from app.controllers.user_controller import user_bp
    from app.controllers.university_controller import university_bp
    from app.controllers.faculty_controller import faculty_bp
    from app.controllers.department_controller import department_bp
    from app.controllers.course_controller import course_bp
    from app.controllers.assignment_controller import assignment_bp
    from app.controllers.submissions_controller import submission_bp
    from app.controllers.registration_controller import registration_bp
    from app.controllers.ai_answer_controller import ai_answer_bp

    app.register_blueprint(user_bp, url_prefix='/users') 
    app.register_blueprint(university_bp, url_prefix='/universities')
    app.register_blueprint(faculty_bp, url_prefix='/faculties')
    app.register_blueprint(department_bp, url_prefix='/department')
    app.register_blueprint(course_bp, url_prefix='/course')
    app.register_blueprint(assignment_bp, url_prefix='/assignments')
    app.register_blueprint(submission_bp, url_prefix='/submission')
    app.register_blueprint(registration_bp, url_prefix='/registration')
    app.register_blueprint(ai_answer_bp, url_prefix='/answer')



    return app
