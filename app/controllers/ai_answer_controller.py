from flask import Blueprint, request, jsonify
from app.models.ai_answer  import Ai_answer
from app import db
from app.utils.decorators import token_required  

ai_answer_bp = Blueprint('ai_answer_bp', __name__)

@ai_answer_bp.route('/register', methods=['POST'])
@token_required
def create_answer():
    data = request.json  
    answer = data.get('answer')

    new_answer = Ai_answer(
        answer = answer
    )

    db.session.add(new_answer)
    db.session.commit()

    return jsonify({'message': 'Respuesta creada satisfactoriamente', 'answer_id':new_answer.answer_id}), 201

@ai_answer_bp.route('/delete', methods=['DELETE']) 
@token_required   
def delete_answer():
    data = request.json
    answer_id = data.get('answer_id')
    answer_delete = Ai_answer.query.filter_by(answer_id=answer_id).first()

    if answer_delete:
        db.session.delete(answer_delete)
        db.session.commit()
        return jsonify({'message': 'Respuesta IA eliminada correctamente'}), 200
    else:
        return jsonify({'message': 'Respuesta IA no encontrada'}), 404

@ai_answer_bp.route('/get/<user_jwt>', methods=['GET'])
@token_required
def read_all_answers(user_jwt):
    answers = Ai_answer.query.all()  

    if not answers:
        return jsonify({'message': 'No hay respuestas IA registradas'}), 404

    answers_list = []
    for answerIA in answers:
        answers_list.append({
            'answer_id': answerIA.answer_id,
            'answer': answerIA.answer       
        })

    return jsonify(answers_list), 200  

@ai_answer_bp.route('/update', methods=['PUT'])      
@token_required
def update_answer():
    data = request.json
    answer_id = data.get('answer_id')

    if not answer_id:
            return jsonify({'message': 'El campo answer_id es requerido'}), 400

    answerIA = Ai_answer.query.filter_by(answer_id=answer_id).first()

    if not answerIA:
        return jsonify({'message': 'Respuesta IA no encontrada'}), 404

    if 'answer' in data:
        answerIA.answer = data['answer'] 

    try:
        db.session.commit() 
        return jsonify({'message': 'Respuesta IA actualizada satisfactoriamente'}), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({'message': 'Error al actualizar respuesta IA en la base de datos', 'error': str(e)}), 500