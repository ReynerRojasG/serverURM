from flask import Blueprint, request, jsonify
from app.models.university import University 
from app import db
from app.utils.decorators import token_required  

university_bp = Blueprint('university_bp', __name__)

@university_bp.route('/register', methods=['POST'])
@token_required 
def create_university():
    data = request.json  
    university_name = data.get('university_name')

    existing_university = University.query.filter_by(university_name=university_name).first()
    if existing_university:
        return jsonify({'message': 'La universidad ya existe'}), 409  

    new_university = University(university_name=university_name)

    db.session.add(new_university)
    db.session.commit()

    return jsonify({'message': 'Universidad creada satisfactoriamente', 'university_id': new_university.university_id}), 201

@university_bp.route('/delete', methods=['DELETE'])
@token_required
def delete_university():
    data = request.json
    university_name = data.get('university_name')
    university_delete = University.query.filter_by(university_name=university_name).first()

    if university_delete:
        db.session.delete(university_delete)
        db.session.commit()
        return jsonify({'message': 'Universidad eliminada correctamente'}), 200
    else:
        return jsonify({'message': 'Universidad no encontrada'}), 404

@university_bp.route('/get/<user_jwt>', methods=['GET'])
@token_required
def read_all_universities(user_jwt):
    universities = University.query.all()  

    if not universities:
        return jsonify({'message': 'No hay universidades registradas'}), 404

    universities_list = []
    for university in universities:
        universities_list.append({
            'university_id': university.university_id,
            'university_name': university.university_name
        })

    return jsonify(universities_list), 200

@university_bp.route('/update', methods=['PUT'])      
@token_required
def update_university():
    data = request.json
    university_id = data.get('university_id')

    if not university_id:
            return jsonify({'message': 'El campo university_id es requerido'}), 400

    university = University.query.filter_by(university_id=university_id).first()

    if not university:
        return jsonify({'message': 'Universidad no encontrada'}), 404

    if 'university_name' in data:
        university.university_name = data['university_name']

    try:
        db.session.commit() 
        return jsonify({'message': 'Universidad actualizada satisfactoriamente'}), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({'message': 'Error al actualizar la universidad en la base de datos', 'error': str(e)}), 500
    
