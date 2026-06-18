from app import db
from decimal import Decimal
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.Enum(
            'admin',
            'manager',
            'hrd',
            'user',
            name='user_role'
        ),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }
    
class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    current_position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'current_position': self.current_position,
            'department': self.department,
            'created_at': self.created_at.isoformat()
        }
    
class Criteria(db.Model):

    __tablename__ = 'criteria'

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(
        db.String(10),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    weight = db.Column(
        db.Numeric(5,4),
        nullable=False
    )

    unit = db.Column(
        db.String(50)
    )

    attribute = db.Column(
        db.String(20),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):

        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'weight': float(self.weight),
            'unit': self.unit,
            'attribute': self.attribute,
            'created_at': self.created_at.isoformat()
        }
    
class Score(db.Model):

    __tablename__ = 'scores'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey('employees.id'),
        nullable=False
    )

    criteria_id = db.Column(
        db.Integer,
        db.ForeignKey('criteria.id'),
        nullable=False
    )

    value = db.Column(
        db.Float,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = (
        db.UniqueConstraint(
            'employee_id',
            'criteria_id',
            name='unique_employee_criteria'
        ),
    )

    def to_dict(self):

        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'criteria_id': self.criteria_id,
            'value': self.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }