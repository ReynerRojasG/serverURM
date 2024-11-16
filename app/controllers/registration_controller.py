from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.registration  import Registration
from app.models.course import Course
from app import db
from app.utils.decorators import token_required  

registration_bp = Blueprint('registration_bp', __name__)

@registration_bp.route('/register', methods=['POST'])
@token_required
def create_registration():
    from app.services.telegram_service import notify_register
    data = request.json 

    student_id = data.get('student_id')
    course_id = data.get('course_id')

    existing_register = Registration.query.filter_by(student_id=student_id, course_id=course_id).first()

    if existing_register:
        return jsonify({'message': 'El estudiante ya esta matriculado'}), 409  

    new_register = Registration(
        student_id=student_id,
        course_id=course_id
    )

    db.session.add(new_register)
    db.session.commit()

    student = User.query.filter_by(user_id=student_id).first()
    course = Course.query.filter_by(course_id=course_id).first()

    if student:
        student_name = student.user_name
    else:
        student_name = "Desconocido"

    if course:
        course_name = course.course_name
    else:
        course_name = "Desconocido"

    notify_register(student_name, course_name)
    return jsonify({'message': 'Estudiante matriculado satisfactoriamente', 'registration_id': new_register.registration_id}), 201

@registration_bp.route('/delete', methods=['DELETE'])
@token_required
def delete_registration():
    data = request.json
    registration_id = data.get('registration_id')
    registration_delete = Registration.query.filter_by(registration_id=registration_id).first()

    if registration_delete:
        db.session.delete(registration_delete)
        db.session.commit()
        return jsonify({'message': 'Matricula eliminada correctamente'}), 200
    else:
        return jsonify({'message': 'Matricula no encontrada'}), 404

@registration_bp.route('/get/<user_jwt>', methods=['GET'])
@token_required
def read_all_registrations(user_jwt):
    registrations = Registration.query.all()  

    if not registrations:
        return jsonify({'message': 'No hay matriculas registradas'}), 404

    registrations_list = []
    for registration in registrations:
        registrations_list.append({
            'registration_id': registration.registration_id,
            'student_id': registration.student_id,
            'course_id': registration.course_id           
        })

    return jsonify(registrations_list), 200  

@registration_bp.route('/update', methods=['PUT'])      
@token_required
def update_registration():
    data = request.json
    registration_id = data.get('registration_id')

    if not registration_id:
            return jsonify({'message': 'El campo registration_id es requerido'}), 400

    registration = Registration.query.filter_by(registration_id=registration_id).first()

    if not registration:
        return jsonify({'message': 'Matricula no encontrada'}), 404

    if 'student_id' in data:
        registration.student_id = data['student_id'] 
    if 'course_id' in data:
        registration.course_id = data['course_id'] 

    try:
        db.session.commit() 
        return jsonify({'message': 'Matricula actualizada satisfactoriamente'}), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({'message': 'Error al actualizar matricula en la base de datos', 'error': str(e)}), 500