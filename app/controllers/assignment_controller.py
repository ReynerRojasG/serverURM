from flask import Blueprint, request, jsonify
from app.models.assignment import Assignment
from app.models.registration import Registration
from app.models.user import User
from app import db
from app.utils.decorators import token_required  
from app.services.telegram_service import notify_assignment

assignment_bp = Blueprint('assignment_bp', __name__)

@assignment_bp.route('/register', methods=['POST'])
@token_required
def create_assignment():
    data = request.json  
    course_id = data.get('course_id')
    professor_id = data.get('professor_id')
    course_statement = data.get('course_statement')
    assignment_type = data.get('assignment_type')
    initial_date = data.get('initial_date')
    final_date = data.get('final_date')

    existing_assignment = Assignment.query.filter_by(
        course_id=course_id,
        professor_id=professor_id,
        assignment_type=assignment_type,
        initial_date=initial_date,
        final_date=final_date
    ).first() 

    if existing_assignment:
        return jsonify({'message': 'Una asignacion similar ya existe'}), 409  

    new_assignment = Assignment(
        course_id=course_id,
        professor_id=professor_id,
        course_statement=course_statement,
        assignment_type=assignment_type,
        initial_date=initial_date,
        final_date=final_date
    )

    db.session.add(new_assignment)
    db.session.commit()

    students_in_course = Registration.query.filter_by(course_id=course_id).all()
    for registration in students_in_course:
        student = User.query.filter_by(user_id=registration.student_id).first()
        if student:
            notify_assignment(student.user_name, initial_date, final_date)

    return jsonify({'message': 'Asignacion creada satisfactoriamente', 'assignment_id': new_assignment.assignment_id}), 201

@assignment_bp.route('/delete', methods=['DELETE'])
@token_required
def delete_assignment():
    data = request.json
    assignment_id = data.get('assignment_id')
    assignment_delete = Assignment.query.filter_by(assignment_id=assignment_id).first()

    if assignment_delete:
        db.session.delete(assignment_delete)
        db.session.commit()
        return jsonify({'message': 'Asignacion eliminada correctamente'}), 200
    else:
        return jsonify({'message': 'Asignacion no encontrada'}), 404


@assignment_bp.route('/get/<user_jwt>', methods=['GET'])
@token_required
def read_all_assignments(user_jwt):
    assignments = Assignment.query.all()  

    if not assignments:
        return jsonify({'message': 'No hay asignaciones registradas'}), 404

    assignments_list = []
    for assignment in assignments:
        assignments_list.append({
            'assignment_id': assignment.assignment_id,
            'course_id': assignment.course_id,
            'professor_id': assignment.professor_id,
            'course_statement': assignment.course_statement,
            'assignment_type': assignment.assignment_type,
            'initial_date': assignment.initial_date,
            'final_date': assignment.final_date
        })

    return jsonify(assignments_list), 200  

@assignment_bp.route('/update', methods=['PATCH'])      
@token_required
def update_assignment():
    data = request.json
    assignment_id = data.get('assignment_id')

    if not assignment_id:
            return jsonify({'message': 'El campo assignment_id es requerido'}), 400

    assignment = Assignment.query.filter_by(assignment_id=assignment_id).first()

    if not assignment:
        return jsonify({'message': 'Asignacion no encontrada'}), 404

    if 'course_id' in data:
        assignment.course_id = data['course_id'] 
    if 'professor_id' in data:
        assignment.professor_id = data['professor_id'] 
    if 'course_statement' in data:
        assignment.course_statement = data['course_statement'] 
    if 'assignment_type' in data:
        assignment.assignment_type = data['assignment_type'] 
    if 'initial_date' in data:
        assignment.initial_date = data['initial_date'] 
    if 'final_date' in data:
        assignment.final_date = data['final_date'] 

    try:
        db.session.commit() 
        return jsonify({'message': 'Asignacion actualizada satisfactoriamente'}), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({'message': 'Error al actualizar la asignacion en la base de datos', 'error': str(e)}), 500