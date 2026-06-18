from flask import Blueprint, request, jsonify
from decimal import Decimal

from app import db
from app.models import Criteria

criteria_bp = Blueprint('criteria', __name__)


# =======================
# CREATE CRITERIA
# =======================
@criteria_bp.route('/', methods=['POST'])
def create_criteria():

    try:

        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                'success': False,
                'message': 'Body harus berupa JSON'
            }), 400

        required_fields = [
            'code',
            'name',
            'weight',
            'attribute'
        ]

        for field in required_fields:

            if field not in data:

                return jsonify({
                    'success': False,
                    'message': f'{field} wajib diisi'
                }), 400

        if data['attribute'] not in ['benefit', 'cost']:

            return jsonify({
                'success': False,
                'message': 'Attribute harus benefit atau cost'
            }), 400

        existing = Criteria.query.filter_by(
            code=data['code']
        ).first()

        if existing:

            return jsonify({
                'success': False,
                'message': 'Kode kriteria sudah ada'
            }), 409

        total_weight = (
            db.session.query(
                db.func.sum(Criteria.weight)
            ).scalar()
            or Decimal('0')
        )

        new_total = (
            total_weight
            + Decimal(str(data['weight']))
        )

        if new_total > Decimal('1'):

            return jsonify({
                'success': False,
                'message': 'Total bobot tidak boleh melebihi 1'
            }), 400

        criteria = Criteria(

            code=data['code'],

            name=data['name'],

            weight=Decimal(
                str(data['weight'])
            ),

            unit=data.get('unit'),

            attribute=data['attribute']
        )

        db.session.add(criteria)

        db.session.commit()

        return jsonify({

            'success': True,

            'message': 'Criteria berhasil dibuat',

            'data': criteria.to_dict()

        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({

            'success': False,

            'message': str(e)

        }), 500


# =======================
# GET ALL
# =======================
@criteria_bp.route('/', methods=['GET'])
def get_criteria():

    try:

        criteria = Criteria.query.order_by(
            Criteria.code.asc()
        ).all()

        return jsonify({

            'success': True,

            'data': [

                c.to_dict()

                for c in criteria

            ]

        }), 200

    except Exception as e:

        return jsonify({

            'success': False,

            'message': str(e)

        }), 500


# =======================
# GET BY ID
# =======================
@criteria_bp.route('/<int:id>', methods=['GET'])
def get_criteria_by_id(id):

    try:

        criteria = Criteria.query.get(id)

        if not criteria:

            return jsonify({

                'success': False,

                'message': 'Criteria tidak ditemukan'

            }), 404

        return jsonify({

            'success': True,

            'data': criteria.to_dict()

        }), 200

    except Exception as e:

        return jsonify({

            'success': False,

            'message': str(e)

        }), 500


# =======================
# UPDATE
# =======================
@criteria_bp.route('/<int:id>', methods=['PUT'])
def update_criteria(id):

    try:

        criteria = Criteria.query.get(id)

        if not criteria:

            return jsonify({

                'success': False,

                'message': 'Criteria tidak ditemukan'

            }), 404

        data = request.get_json(silent=True)

        if not data:

            return jsonify({

                'success': False,

                'message': 'Body harus berupa JSON'

            }), 400

        old_weight = criteria.weight

        new_weight = Decimal(

            str(

                data.get(

                    'weight',

                    old_weight

                )

            )

        )

        total_weight = (

            db.session.query(

                db.func.sum(Criteria.weight)

            ).scalar()

            or Decimal('0')

        )

        total_weight = (

            total_weight

            - old_weight

            + new_weight

        )

        if total_weight > Decimal('1'):

            return jsonify({

                'success': False,

                'message': 'Total bobot tidak boleh melebihi 1'

            }), 400

        if 'attribute' in data:

            if data['attribute'] not in [

                'benefit',

                'cost'

            ]:

                return jsonify({

                    'success': False,

                    'message': 'Attribute harus benefit atau cost'

                }), 400

        criteria.code = data.get(

            'code',

            criteria.code

        )

        criteria.name = data.get(

            'name',

            criteria.name

        )

        criteria.weight = new_weight

        criteria.unit = data.get(

            'unit',

            criteria.unit

        )

        criteria.attribute = data.get(

            'attribute',

            criteria.attribute

        )

        db.session.commit()

        return jsonify({

            'success': True,

            'message': 'Criteria berhasil diperbarui',

            'data': criteria.to_dict()

        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({

            'success': False,

            'message': str(e)

        }), 500


# =======================
# DELETE
# =======================
@criteria_bp.route('/<int:id>', methods=['DELETE'])
def delete_criteria(id):

    try:

        criteria = Criteria.query.get(id)

        if not criteria:

            return jsonify({

                'success': False,

                'message': 'Criteria tidak ditemukan'

            }), 404

        db.session.delete(criteria)

        db.session.commit()

        return jsonify({

            'success': True,

            'message': 'Criteria berhasil dihapus'

        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({

            'success': False,

            'message': str(e)

        }), 500