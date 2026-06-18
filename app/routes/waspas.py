from flask import Blueprint, jsonify

from app import db
from app.models import Employee, Criteria, Score, Waspas

waspas_bp = Blueprint('waspas', __name__)

@waspas_bp.route('/calculate', methods=['GET'])
def calculate_waspas():

    try:

        lambda_value = 0.5

        employees = Employee.query.all()

        criteria = Criteria.query.all()

        if not employees:

            return jsonify({
                'success': False,
                'message': 'Data employee kosong'
            }), 400

        if not criteria:

            return jsonify({
                'success': False,
                'message': 'Data criteria kosong'
            }), 400

        matrix = {}

        for employee in employees:

            matrix[employee.id] = {}

            for criterion in criteria:

                score = Score.query.filter_by(

                    employee_id=employee.id,

                    criteria_id=criterion.id

                ).first()

                if not score:

                    return jsonify({

                        'success': False,

                        'message': f'{employee.name} belum memiliki nilai lengkap'

                    }), 400

                matrix[employee.id][criterion.id] = score.value

        normalization = {}

        for criterion in criteria:

            values = [

                matrix[emp.id][criterion.id]

                for emp in employees

            ]

            max_value = max(values)

            min_value = min(values)

            for employee in employees:

                normalization.setdefault(
                    employee.id,
                    {}
                )

                value = matrix[
                    employee.id
                ][criterion.id]

                if criterion.attribute == 'benefit':

                    normalized = value / max_value

                else:

                    normalized = min_value / value

                normalization[
                    employee.id
                ][criterion.id] = normalized

        results = []

        for employee in employees:

            q1 = 0

            q2 = 1

            for criterion in criteria:

                weight = float(
                    criterion.weight
                )

                value = normalization[
                    employee.id
                ][criterion.id]

                q1 += value * weight

                q2 *= pow(
                    value,
                    weight
                )

            q_final = (

                lambda_value * q1

            ) + (

                (1 - lambda_value) * q2

            )

            results.append({

                'employee_id': employee.id,

                'employee_name': employee.name,

                'q1_wsm': round(q1, 6),

                'q2_wpm': round(q2, 6),

                'q_final': round(q_final, 6)

            })

        results.sort(

            key=lambda x: x['q_final'],

            reverse=True

        )

        Waspas.query.delete()

        db.session.commit()

        for index, item in enumerate(

            results,

            start=1

        ):

            waspas = Waspas(

                employee_id=item['employee_id'],

                q1_wsm=item['q1_wsm'],

                q2_wpm=item['q2_wpm'],

                q_final=item['q_final'],

                rank=index,

                lambda_value=lambda_value

            )

            db.session.add(waspas)

            item['rank'] = index

        db.session.commit()

        return jsonify({

            'success': True,

            'message': 'Perhitungan WASPAS berhasil',

            'data': results

        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({

            'success': False,

            'message': str(e)

        }), 500
    

@waspas_bp.route('/result', methods=['GET'])
def get_result():

    try:

        results = Waspas.query.order_by(

            Waspas.rank.asc()

        ).all()

        data = []

        for item in results:

            employee = Employee.query.get(

                item.employee_id

            )

            data.append({

                'employee_id': item.employee_id,

                'employee_name': employee.name,

                'q1_wsm': item.q1_wsm,

                'q2_wpm': item.q2_wpm,

                'q_final': item.q_final,

                'rank': item.rank

            })

        return jsonify({

            'success': True,

            'data': data

        }), 200

    except Exception as e:

        return jsonify({

            'success': False,

            'message': str(e)

        }), 500