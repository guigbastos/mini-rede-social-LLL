from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/', methods=['POST'])
def register_user():
    """
    ---
    tags:
       - Users
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
              example: Guilherme
            email:
              type: string
              example: guilherme@mail.com
            password:
              type: string
              example: secure_password_123
    responses:
        201:
          description: User created successfully
        400:
          description: Validation error
        500:
          description: Internal server error
    """
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error":"Username, mail and password are required."}), 400
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
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"error": "An internal server error occurred."}), 500
    
@user_bp.route('/login', methods=['POST'])
def login():
    """
    ---
    tags:
       - Users
    parameters:
       - in: body
         name: body
         required: true
         schema:
           type: object
           required:
             - email
             - password
           properties:
             email:
               type: string
               example: guilherme@mail.com
             password:
               type: string
               example: secure_password_123
    responses:
       200:
         description: Login successful
       400:
         description: Validation error
       401:
         description: unauthorized
       500:
         description: Internal server error
    """
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error":"Mail and password are required."}), 400
    
    try: 
        user = UserService.authenticate(
            email=data['email'],
            password=data['password']
        )

        if not user: 
            return jsonify({"error":"Mail or password are incorrect."}), 401
        
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
    """
    ---
    tags:
       - Users
    security:
      - Bearer: []
    parameters:
       - in: path
         name: user_id
         type: integer
         required: true
         description: ID of the user to follow
    responses:
       200:
        description: User followed successfully
       400:
        description: Validation error (e.g., trying to follow yourself)
       401:
        description: Missing or invalid token
       500:
        description: Internal server error
    """
    current_user_id = int(get_jwt_identity())

    try:
        UserService.follow_user(
            follower_id = current_user_id,
            followed_id = user_id
        )
        return jsonify({"message": "You started following this user."}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"error": "An internal server error occurred."}), 500
    
@user_bp.route('/<int:user_id>/unfollow', methods=['POST'])
@jwt_required()
def unfollow(user_id):
    """
    ---
    tags:
       - Users
    security:
      - Bearer: []
    parameters:
       - in: path
         name: user_id
         type: integer
         required: true
         description: ID of the user to unfollow
    responses:
       200:
        description: User unfollowed successfully
       400:
        description: Validation error (e.g., trying to unfollow yourself)
       401:
        description: Missing or invalid token
       500:
        description: Internal server error
    """
    current_user_id = int(get_jwt_identity())

    try: 
        UserService.unfollow_user(
            follower_id = current_user_id,
            followed_id = user_id
        )
        return jsonify({"message": "You stopped following this user."}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        import traceback
        traceback.print_exc()

    return jsonify({"error": "An internal server error occurred."}), 500

