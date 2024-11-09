from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app import db  
import jwt
import datetime
from app.utils.decorators import token_required  

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    university_id = data.get('university_id')
    user_name = data.get('user_name')
    user_password = data.get('user_password')
    user_type = data.get('user_type')
    user_identification = data.get('user_identification')

    existing_user = User.query.filter_by(user_name=user_name).first()
    if existing_user:
        return jsonify({'message': 'El usuario ya existe'}), 409  

    new_user = User(
        university_id=university_id,
        user_name=user_name,
        user_password=user_password,  
        user_type=user_type,
        user_identification=user_identification
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario creado satisfactoriamente'}), 201  

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data.get('id')  
    password = data.get('password')  

    user = User.query.filter_by(user_name=username, user_password=password).first()

    if user:
        token = jwt.encode({
            'user': user.user_name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'jwt': token, 'userID': user.user_id, 'Uid': user.university_id, 'name': user.user_name, 'type': user.user_type, 'userCed': user.user_identification})

    return jsonify({'message': 'Login fallido'}), 401

@user_bp.route('/delete', methods=['DELETE'])
@token_required
def delete_user():
    data = request.json
    user_name = data.get('user_name')
    user_delete = User.query.filter_by(user_name=user_name).first()

    if user_delete:
        db.session.delete(user_delete)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado correctamente'}), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

@user_bp.route('/get/<user_jwt>', methods=['GET'])
@token_required
def read_all_users(user_jwt):
    users = User.query.all()  

    if not users:
        return jsonify({'message': 'No hay usuarios registrados'}), 404

    users_list = []
    for user in users:
        users_list.append({
            'user_id': user.user_id,
            'university_id': user.university_id,
            'user_name': user.user_name,
            'user_type': user.user_type,
            'user_password': user.user_password,
            'user_identification': user.user_identification
        })

    return jsonify(users_list), 200 

@user_bp.route('/update', methods=['PATCH'])      
@token_required
def update_user():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
            return jsonify({'message': 'El campo user_id es requerido'}), 400

    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    if 'university_id' in data:
        user.university_id = data['university_id']
    if 'user_name' in data:
        user.user_name = data['user_name']
    if 'user_type' in data:
        user.user_type = data['user_type']
    if 'user_password' in data:
        user.user_password = data['user_password']
    if 'user_identification' in data:
        user.user_identification = data['user_identification']  

    try:
        db.session.commit()
        return jsonify({'message': 'Usuario actualizado satisfactoriamente'}), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({'message': 'Error al actualizar el usuario en la base de datos', 'error': str(e)}), 500