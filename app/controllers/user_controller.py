from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/', methods=['POST'])
def register_user():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"Erro":"Os campos username, email e password são obrigatórios."}), 400
    try:
        new_user = UserService.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return jsonify({
            "mensagem": "Usuário criado com sucesso!",
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role
        }), 201
    except ValueError as e:
        return jsonify({"Erro": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"Erro": "Ocorreu um erro interno no servidor."}), 500
    
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"Erro":"Os campos email e senha são obrigatórios."}), 400
    
    try: 
        user = UserService.authenticate(
            email=data['email'],
            password=data['password']
        )

        if not user: 
            return jsonify({"Erro":"Email e/ou senha incorretos."}), 401
        
        token = create_access_token(identity=str(user.id))

        return jsonify({
            "mensagem": "Login realizado com sucesso!",
            "token": token
        }), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"erro": "Ocorreu um erro interno no servidor.", "detalhes": str(e)}), 500
    
@user_bp.route('/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def follow(user_id):
    current_user_id = int(get_jwt_identity())

    try:
        UserService.follow_user(
            follower_id = current_user_id,
            followed_id = user_id
        )
        return jsonify({"mensagem": "Você começou a seguir este usuário."}), 200
    
    except ValueError as e:
        return jsonify({"Erro": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"Erro": "Ocorreu um erro interno no servidor."}), 500
    
@user_bp.route('/<int:user_id>/unfollow', methods=['POST'])
@jwt_required()
def unfollow(user_id):
    current_user_id = int(get_jwt_identity())

    try: 
        UserService.unfollow_user(
            follower_id = current_user_id,
            followed_id = user_id
        )
        return jsonify({"mensagem": "Você deixou de seguir este usuário."}), 200
    
    except ValueError as e:
        return jsonify({"Erro": str(e)}), 400

    except Exception as e:
        import traceback
        traceback.print_exc()

    return jsonify({"Erro": "Ocorreu um erro interno no servidor."}), 500

