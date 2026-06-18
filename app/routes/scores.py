from flask import Blueprint, request, jsonify

from app import db
from app.models import Score, Employee, Criteria

scores_bp = Blueprint('scores', __name__)

@scores_bp.route('/employee/<int:employee_id>', methods=['GET'])
def get_employee_scores(employee_id):

    try:

        employee = Employee.query.get(employee_id)

        if not employee:

            return jsonify({
                'success': False,
                'message': 'Employee tidak ditemukan'
            }), 404

        scores = Score.query.filter_by(
            employee_id=employee_id
        ).all()

        data = []

        for score in scores:

            criteria = Criteria.query.get(
                score.criteria_id
            )

            data.append({

                'score_id': score.id,

                'criteria_id': score.criteria_id,

                'criteria_name': criteria.name,

                'value': score.value

            })

        return jsonify({

            'success': True,

            'employee_id': employee_id,

            'data': data

        }), 200

    except Exception as e:

        return jsonify({

            'success': False,

            'message': str(e)

        }), 500
    
@scores_bp.route('/employee/<int:employee_id>', methods=['POST'])
def create_scores(employee_id):

    try:

        employee = Employee.query.get(employee_id)

        if not employee:

            return jsonify({

                'success': False,

                'message': 'Employee tidak ditemukan'

            }), 404

        data = request.get_json()

        scores = data.get('scores')

        if not scores:

            return jsonify({

                'success': False,

                'message': 'scores wajib diisi'

            }), 400

        inserted = []

        for item in scores:

            criteria_id = item.get('criteria_id')

            value = item.get('value')

            criteria = Criteria.query.get(criteria_id)

            if not criteria:

                continue

            existing = Score.query.filter_by(

                employee_id=employee_id,

                criteria_id=criteria_id

            ).first()

            if existing:

                continue

            score = Score(

                employee_id=employee_id,

                criteria_id=criteria_id,

                value=value

            )

            db.session.add(score)

            inserted.append(score)

        db.session.commit()

        return jsonify({

            'success': True,

            'message': 'Nilai berhasil ditambahkan'

        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({

            'success': False,

            'message': str(e)

        }), 500
    
@scores_bp.route('/employee/<int:employee_id>', methods=['PUT'])
def update_scores(employee_id):

    try:

        employee = Employee.query.get(employee_id)

        if not employee:

            return jsonify({

                'success': False,

                'message': 'Employee tidak ditemukan'

            }), 404

        data = request.get_json()

        scores = data.get('scores')

        if not scores:

            return jsonify({

                'success': False,

                'message': 'scores wajib diisi'

            }), 400

        for item in scores:

            criteria_id = item.get('criteria_id')

            value = item.get('value')

            score = Score.query.filter_by(

                employee_id=employee_id,

                criteria_id=criteria_id

            ).first()

            if score:

                score.value = value

        db.session.commit()

        return jsonify({

            'success': True,

            'message': 'Nilai berhasil diperbarui'

        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({

            'success': False,

            'message': str(e)

        }), 500
    
@scores_bp.route('/<int:id>', methods=['DELETE'])
def delete_score(id):

    try:

        score = Score.query.get(id)

        if not score:

            return jsonify({

                'success': False,

                'message': 'Score tidak ditemukan'

            }), 404

        db.session.delete(score)

        db.session.commit()

        return jsonify({

            'success': True,

            'message': 'Score berhasil dihapus'

        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({

            'success': False,

            'message': str(e)

        }), 500
    
@scores_bp.route('/', methods=['GET'])
def get_all_scores():

    try:

        scores = Score.query.all()

        data = []

        for score in scores:

            employee = Employee.query.get(
                score.employee_id
            )

            criteria = Criteria.query.get(
                score.criteria_id
            )

            data.append({

                'score_id': score.id,

                'employee_id': score.employee_id,

                'employee_name': employee.name,

                'criteria_id': score.criteria_id,

                'criteria_name': criteria.name,

                'value': score.value

            })

        return jsonify({

            'success': True,

            'total': len(data),

            'data': data

        }), 200

    except Exception as e:

        return jsonify({

            'success': False,

            'message': str(e)

        }), 500