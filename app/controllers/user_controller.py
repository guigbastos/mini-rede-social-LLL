from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/', methods=['POST'])
def register_user():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"Error":"Username, mail and password are required."}), 400
    try:
        new_user = UserService.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return jsonify({
            "message": "User created successfully!",
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role
        }), 201
    except ValueError as e:
        return jsonify({"Error": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"Error": "An internal server error occurred."}), 500
    
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"Error":"Mail and password are required."}), 400
    
    try: 
        user = UserService.authenticate(
            email=data['email'],
            password=data['password']
        )

        if not user: 
            return jsonify({"Error":"Mail or password are incorrect."}), 401
        
        token = create_access_token(identity=str(user.id))

        return jsonify({
            "message": "Login successful!",
            "token": token
        }), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"error": "An internal server error occurred.", "details": str(e)}), 500
    
@user_bp.route('/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def follow(user_id):
    current_user_id = int(get_jwt_identity())

    try:
        UserService.follow_user(
            follower_id = current_user_id,
            followed_id = user_id
        )
        return jsonify({"message": "You started following this user."}), 200
    
    except ValueError as e:
        return jsonify({"Error": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"Error": "An internal server error occurred."}), 500
    
@user_bp.route('/<int:user_id>/unfollow', methods=['POST'])
@jwt_required()
def unfollow(user_id):
    current_user_id = int(get_jwt_identity())

    try: 
        UserService.unfollow_user(
            follower_id = current_user_id,
            followed_id = user_id
        )
        return jsonify({"message": "You stopped following this user."}), 200
    
    except ValueError as e:
        return jsonify({"Error": str(e)}), 400

    except Exception as e:
        import traceback
        traceback.print_exc()

    return jsonify({"Error": "An internal server error occurred."}), 500

