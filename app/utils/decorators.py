from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.get_json()
        token = None

        if request.method in ['POST', 'DELETE', 'PATCH'] and data:
            token = data.get('user_jwt')

        if not token:
            token = kwargs.get('user_jwt')

        if not token:
            return jsonify({'message': 'No enviaste tu token'}), 403
        
        try:
            jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token invalido'}), 403

        return f(*args, **kwargs)

    return decorated
