from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.submission import Submission
from app.models.assignment import Assignment
from app import db
from app.utils.decorators import token_required  

submission_bp = Blueprint('submission_bp', __name__)

@submission_bp.route('/register', methods=['POST'])
@token_required
def create_submission():
    from app.services.telegram_service import notify_submission
    data = request.json  

    required_fields = ['assignment_id', 'student_id', 'submission_date', 'submission_file', 'submission_status']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'El campo {field} es requerido'}), 400

    submission_score = data.get('submission_score')
    assignment_id = data.get('assignment_id')
    student_id = data.get('student_id')
    submission_date = data.get('submission_date')
    submission_file = data.get('submission_file')
    submission_status = data.get('submission_status')
    comment_ai = data.get('comment_ai') 
    comment_professor = data.get('comment_professor') 

    new_submission = Submission(
        submission_score=submission_score,
        assignment_id=assignment_id,
        student_id=student_id,
        submission_date=submission_date,
        submission_file=submission_file,
        submission_status=submission_status,
        comment_ai=comment_ai,
        comment_professor=comment_professor
    )

    try:
        db.session.add(new_submission)
        db.session.commit()

        assignment = Assignment.query.filter_by(assignment_id=assignment_id).first()
        if assignment:
            professor_id = assignment.professor_id
            
            professor = User.query.filter_by(user_id=professor_id).first()
            if professor:
                professor_name = professor.user_name
                if submission_status == "No revisado" or submission_status is None:
                    notify_submission(professor_name)

        return jsonify({'message': 'Entrega ralizada satisfactoriamente', 'submission_id': new_submission.submission_id}), 201
    except Exception as e:
        db.session.rollback()  
        return jsonify({'message': 'Error al entregar la asignacion', 'error': str(e)}), 500

@submission_bp.route('/delete', methods=['DELETE'])
@token_required
def delete_submission():
    data = request.json
    submission_id = data.get('submission_id')
    submission_delete = Submission.query.filter_by(submission_id=submission_id).first()

    if submission_delete:
        db.session.delete(submission_delete)
        db.session.commit()
        return jsonify({'message': 'Entrega eliminada correctamente'}), 200
    else:
        return jsonify({'message': 'Entrega no encontrada'}), 404

@submission_bp.route('/get/<user_jwt>', methods=['GET'])
@token_required
def read_all_submissions(user_jwt):
    submissions = Submission.query.all()  

    if not submissions:
        return jsonify({'message': 'No hay entregas registradas'}), 404

    submissions_list = []
    for submission in submissions:
        submissions_list.append({
            'submission_id': submission.submission_id,
            'submission_score': submission.submission_score,
            'assignment_id': submission.assignment_id,
            'student_id': submission.student_id,
            'submission_date': submission.submission_date,
            'submission_file': submission.submission_file,
            'submission_status': submission.submission_status,
            'comment_ai': submission.comment_ai,
            'comment_professor': submission.comment_professor
        })

    return jsonify(submissions_list), 200  

@submission_bp.route('/update', methods=['PUT']) 
@token_required
def update_submission():
    from app.services.telegram_service import notify_score
    data = request.json
    submission_id = data.get('submission_id')

    if not submission_id:
        return jsonify({'message': 'El campo submission_id es requerido'}), 400

    submission = Submission.query.filter_by(submission_id=submission_id).first()

    if not submission:
        return jsonify({'message': 'Entrega no encontrada'}), 404

    score_updated = False
    if 'submission_score' in data:
        submission.submission_score = data['submission_score']
        score_updated = True
    if 'comment_ai' in data:
        submission.comment_ai = data['comment_ai']
    if 'comment_professor' in data:
        submission.comment_professor = data['comment_professor']   
    if 'submission_status' in data:
        submission.submission_status = data['submission_status']   
    if 'submission_file' in data:
        submission.submission_file = data['submission_file']   
    if 'submission_date' in data:
        submission.submission_date = data['submission_date']      

    try:
        db.session.commit()
        if score_updated:
            student = User.query.filter_by(user_id=submission.student_id).first()
            if student:
                notify_score(student.user_name, submission.submission_score)
        return jsonify({'message': 'Entrega actualizada satisfactoriamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al actualizar la entrega', 'error': str(e)}), 500

