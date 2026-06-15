from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from app.routes.auth import auth_bp
    from app.routes.criteria import criteria_bp
    from app.routes.weights import weights_bp
    from app.routes.employees import employees_bp
    from app.routes.scores import scores_bp
    from app.routes.waspas import waspas_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(criteria_bp, url_prefix='/api/criteria')
    app.register_blueprint(weights_bp, url_prefix='/api/weights')
    app.register_blueprint(employees_bp, url_prefix='/api/employees')
    app.register_blueprint(scores_bp, url_prefix='/api/scores')
    app.register_blueprint(waspas_bp, url_prefix='/api/waspas')

    with app.app_context():
        db.create_all()

    return app