from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:lagunalivinglab2026@localhost:5432/rede_social_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'laguna-living-lab-2026'
    
    db.init_app(app)
    jwt.init_app(app)

    from app.models.user import User
    from app.models.post import Post

    with app.app_context():
        db.create_all()

    from app.controllers.user_controller import user_bp
    app.register_blueprint(user_bp)

    from app.controllers.post_controller import post_bp
    app.register_blueprint(post_bp)

    @app.route("/")
    def index():
        return 'Arquitetura em camadas configurada com sucesso!'
    
    return app
