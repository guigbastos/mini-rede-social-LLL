from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from flasgger import Swagger

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    db.init_app(app)
    jwt.init_app(app)

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Social Network API",
            "description": "Interactive API documentation for the Social Network backend",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
            }
        }
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    from app.models.user import User
    from app.models.post import Post
    from app.models.comment import Comment

    with app.app_context():
        db.create_all()

    from app.controllers.user_controller import user_bp
    app.register_blueprint(user_bp)

    from app.controllers.post_controller import post_bp
    app.register_blueprint(post_bp)

    from app.controllers.comment_controller import comment_bp
    app.register_blueprint(comment_bp)

    @app.route("/")
    def index():
        return 'Arquitetura em camadas configurada com sucesso!'
    
    return app
