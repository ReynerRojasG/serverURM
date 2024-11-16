from flask import Blueprint, request, jsonify
from app.models.department import Department
from app import db
from app.utils.decorators import token_required  

department_bp = Blueprint('department_bp', __name__)

@department_bp.route('/register', methods=['POST'])
@token_required
def create_department():
    data = request.json  
    department_name = data.get('department_name')
    department_information = data.get('department_information')
    faculty_id = data.get('faculty_id')

    existing_department = Department.query.filter_by(department_name=department_name).first()
    if existing_department:
        return jsonify({'message': 'El departamento ya existe'}), 409  

    new_department = Department(
        department_name = department_name, 
        department_information = department_information, 
        faculty_id = faculty_id
    )

    db.session.add(new_department)
    db.session.commit()

    return jsonify({'message': 'Departamento creada satisfactoriamente', 'department_id':new_department.department_id}), 201

@department_bp.route('/delete', methods=['DELETE'])
@token_required
def delete_department():
    data = request.json
    department_name = data.get('department_name')
    department_delete = Department.query.filter_by(department_name=department_name).first()

    if department_delete:
        db.session.delete(department_delete)
        db.session.commit()
        return jsonify({'message': 'Departamento eliminado correctamente'}), 200
    else:
        return jsonify({'message': 'Departmento no encontrado'}), 404

@department_bp.route('/get/<user_jwt>', methods=['GET'])
@token_required
def read_all_departments(user_jwt):
    departments = Department.query.all()  

    if not departments:
        return jsonify({'message': 'No hay departamentos registrados'}), 404

    departments_list = []
    for department in departments:
        departments_list.append({
            'department_id': department.department_id,
            'department_name': department.department_name,
            'department_information': department.department_information,
            'faculty_id': department.faculty_id
        })

    return jsonify(departments_list), 200    
 
@department_bp.route('/update', methods=['PUT'])      
@token_required
def update_department():
    data = request.json
    department_id = data.get('department_id')

    if not department_id:
            return jsonify({'message': 'El campo department_id es requerido'}), 400

    department = Department.query.filter_by(department_id=department_id).first()

    if not department:
        return jsonify({'message': 'Departamento no encontrado'}), 404

    if 'department_name' in data:
        department.department_name = data['department_name'] 
    if 'department_information' in data:
        department.department_information = data['department_information'] 
    if 'faculty_id' in data:
        department.faculty_id = data['faculty_id'] 

    try:
        db.session.commit() 
        return jsonify({'message': 'Departamento actualizado satisfactoriamente'}), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({'message': 'Error al actualizar el departamento en la base de datos', 'error': str(e)}), 500