from flask import Blueprint, request, jsonify
from app.models.faculty import Faculty
from app import db
from app.utils.decorators import token_required  

faculty_bp = Blueprint('faculty_bp', __name__)

@faculty_bp.route('/register', methods=['POST'])
@token_required
def create_faculty():
    data = request.json  
    faculty_name = data.get('faculty_name')
    faculty_information = data.get('faculty_information')
    university_id = data.get('university_id')

    existing_faculty = Faculty.query.filter_by(faculty_name=faculty_name).first()
    if existing_faculty:
        return jsonify({'message': 'La facultad ya existe'}), 409  

    new_faculty = Faculty(
        faculty_name = faculty_name, 
        faculty_information = faculty_information, 
        university_id = university_id
    )

    db.session.add(new_faculty)
    db.session.commit()

    return jsonify({'message': 'Facultad creada satisfactoriamente', 'faculty_id':new_faculty.faculty_id}), 201

@faculty_bp.route('/delete', methods=['DELETE'])
@token_required
def delete_faculty():
    data = request.json
    faculty_name = data.get('faculty_name')   
    faculty_delete = Faculty.query.filter_by(faculty_name=faculty_name).first()

    if faculty_delete:
        db.session.delete(faculty_delete)
        db.session.commit()
        return jsonify({'message': 'Facultad eliminada correctamente'}), 200
    else:
        return jsonify({'message': 'Facultad no encontrada'}), 404

@faculty_bp.route('/get/<user_jwt>', methods=['GET'])
@token_required
def read_all_faculties(user_jwt):
    faculties = Faculty.query.all()  

    if not faculties:
        return jsonify({'message': 'No hay facultades registradas'}), 404

    faculties_list = []
    for faculty in faculties:
        faculties_list.append({
            'faculty_id': faculty.faculty_id,
            'faculty_name': faculty.faculty_name,
            'faculty_information': faculty.faculty_information,
            'university_id': faculty.university_id
        })

    return jsonify(faculties_list), 200        


@faculty_bp.route('/update', methods=['PUT'])      
@token_required
def update_faculty():
    data = request.json
    faculty_id = data.get('faculty_id')

    if not faculty_id:
            return jsonify({'message': 'El campo faculty_id es requerido'}), 400

    faculty = Faculty.query.filter_by(faculty_id=faculty_id).first()
    if not faculty:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    
    if 'faculty_name' in data:
        faculty.faculty_name = data['faculty_name']    
    if 'faculty_information' in data:
        faculty.faculty_information = data['faculty_information']
    if 'university_id' in data:
        faculty.university_id = data['university_id']

    try:
        db.session.commit()
        return jsonify({'message': 'Facultad actualizada satisfactoriamente'}), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({'message': 'Error al actualizar la facultad en la base de datos', 'error': str(e)}), 500