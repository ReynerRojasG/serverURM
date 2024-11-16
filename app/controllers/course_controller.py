from flask import Blueprint, request, jsonify
from app.models.course import Course
from app import db
from app.utils.decorators import token_required  

course_bp = Blueprint('course_bp', __name__)

@course_bp.route('/register', methods=['POST'])
@token_required
def create_course():
    data = request.json  
    professor_id = data.get('professor_id')
    department_id = data.get('department_id')
    course_name = data.get('course_name')
    course_information = data.get('course_information')

    existing_course = Course.query.filter_by(course_name=course_name).first()
    if existing_course:
        return jsonify({'message': 'El curso ya existe'}), 409  

    new_course = Course(
        professor_id = professor_id, 
        department_id = department_id,
        course_name = course_name,
        course_information = course_information
    )

    db.session.add(new_course)
    db.session.commit()

    return jsonify({'message': 'Curso creado satisfactoriamente', 'course_id':new_course.course_id}), 201

@course_bp.route('/delete', methods=['DELETE'])
@token_required
def delete_course():
    data = request.json
    course_name = data.get('course_name')
    course_delete = Course.query.filter_by(course_name=course_name).first()

    if course_delete:
        db.session.delete(course_delete)
        db.session.commit()
        return jsonify({'message': 'Curso eliminado correctamente'}), 200
    else:
        return jsonify({'message': 'Curso no encontrado'}), 404

@course_bp.route('/get/<user_jwt>', methods=['GET'])
@token_required
def read_all_courses(user_jwt):
    courses = Course.query.all()  

    if not courses:
        return jsonify({'message': 'No hay cursos registrados'}), 404

    courses_list = []
    for course in courses:
        courses_list.append({
            'course_id': course.course_id,
            'professor_id': course.professor_id,
            'department_id': course.department_id,
            'course_name': course.course_name,
            'course_information': course.course_information
        })

    return jsonify(courses_list), 200   

@course_bp.route('/update', methods=['PUT'])      
@token_required
def update_course():
    data = request.json
    course_id = data.get('course_id')

    if not course_id:
            return jsonify({'message': 'El campo course_id es requerido'}), 400

    course = Course.query.filter_by(course_id=course_id).first()

    if not course:
        return jsonify({'message': 'Curso no encontrado'}), 404

    if 'professor_id' in data:
        course.professor_id = data['professor_id'] 
    if 'department_id' in data:
        course.department_id = data['department_id'] 
    if 'course_name' in data:
        course.course_name = data['course_name'] 
    if 'course_information' in data:
        course.course_information = data['course_information'] 

    try:
        db.session.commit() 
        return jsonify({'message': 'Curso actualizado satisfactoriamente'}), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({'message': 'Error al actualizar el curso en la base de datos', 'error': str(e)}), 500