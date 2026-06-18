from flask import Blueprint, request, jsonify
from app import db
from app.models import Employee

employees_bp = Blueprint('employees', __name__)

# CREATE
@employees_bp.route('/', methods=['POST'])
def create_employee():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Request body is required"
            }), 400

        name = data.get('name')
        current_position = data.get('current_position')
        department = data.get('department')

        if not all([name, current_position, department]):
            return jsonify({
                "success": False,
                "message": "All fields are required"
            }), 400

        employee = Employee(
            name=name,
            current_position=current_position,
            department=department
        )

        db.session.add(employee)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Employee created successfully",
            "data": employee.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# GET ALL
@employees_bp.route('/', methods=['GET'])
def get_employees():
    try:
        employees = Employee.query.order_by(Employee.id.desc()).all()

        return jsonify({
            "success": True,
            "data": [employee.to_dict() for employee in employees]
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# GET BY ID
@employees_bp.route('/<int:id>', methods=['GET'])
def get_employee(id):
    try:
        employee = Employee.query.get(id)

        if not employee:
            return jsonify({
                "success": False,
                "message": "Employee not found"
            }), 404

        return jsonify({
            "success": True,
            "data": employee.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# UPDATE
@employees_bp.route('/<int:id>', methods=['PUT'])
def update_employee(id):
    try:
        employee = Employee.query.get(id)

        if not employee:
            return jsonify({
                "success": False,
                "message": "Employee not found"
            }), 404

        data = request.get_json()

        employee.name = data.get('name', employee.name)
        employee.current_position = data.get(
            'current_position',
            employee.current_position
        )
        employee.department = data.get(
            'department',
            employee.department
        )

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Employee updated successfully",
            "data": employee.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# DELETE
@employees_bp.route('/<int:id>', methods=['DELETE'])
def delete_employee(id):
    try:
        employee = Employee.query.get(id)

        if not employee:
            return jsonify({
                "success": False,
                "message": "Employee not found"
            }), 404

        db.session.delete(employee)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Employee deleted successfully"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500