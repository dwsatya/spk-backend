from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User
import bcrypt

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Data tidak ditemukan'}), 400

    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    role = data.get('role', 'user')

    if not email or not password or not name:
        return jsonify({
            'message': 'Nama, email, dan password wajib diisi'
        }), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            'message': 'Email sudah digunakan'
        }), 409

    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    new_user = User(
        name=name,
        email=email,
        password_hash=password_hash,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'Registrasi berhasil',
        'user': new_user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Data tidak ditemukan'
        }), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({
            'message': 'Email dan password wajib diisi'
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            'message': 'Email atau password salah'
        }), 401

    password_valid = bcrypt.checkpw(
        password.encode('utf-8'),
        user.password_hash.encode('utf-8')
    )

    if not password_valid:
        return jsonify({
            'message': 'Email atau password salah'
        }), 401

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    return jsonify([
        user.to_dict() for user in users
    ]), 200

@auth_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({
            'message': 'User tidak ditemukan'
        }), 404

    return jsonify(user.to_dict()), 200

@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({
            'message': 'User tidak ditemukan'
        }), 404

    data = request.get_json()

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)

    db.session.commit()

    return jsonify({
        'message': 'User berhasil diupdate',
        'user': user.to_dict()
    }), 200

@auth_bp.route('/users/<int:user_id>/password', methods=['PUT'])
def update_password(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({
            'message': 'User tidak ditemukan'
        }), 404

    data = request.get_json()

    password = data.get('password')

    if not password:
        return jsonify({
            'message': 'Password wajib diisi'
        }), 400

    user.password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    db.session.commit()

    return jsonify({
        'message': 'Password berhasil diperbarui'
    }), 200

@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({
            'message': 'User tidak ditemukan'
        }), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        'message': 'User berhasil dihapus'
    }), 200

