from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.post_service import PostService
from app.repositories.user_repository import UserRepository

post_bp = Blueprint('posts', __name__, url_prefix='/posts')

@post_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    """
    ---
    tags:
       - Posts
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - content
          properties:
            content:
              type: string
              example: "This is my first post!"
    responses:
      201:
        description: Post created successfully
      400:
        description: Validation error (e.g., empty content)
      401:
        description: Missing or invalid token
      500:
        description: Internal server error
    """
    data = request.get_json()

    current_user_id = get_jwt_identity()

    if not data or not data.get('content'):
        return jsonify({"error": "Post content cannot be empty."})
    
    try: 
        new_post = PostService.create_post(
            author_id=current_user_id,
            content=data['content']
        )
        return jsonify({
            "message": "Post created successfully!",
            "id": new_post.id,
            "content": new_post.content,
            "created_at": new_post.created_at.isoformat(),
            "author_id": new_post.author_id,
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred."}), 500
    
@post_bp.route('/', methods=['GET'])
@jwt_required()
def get_feed():
    """
    ---
    tags:
       - Posts
    security:
      - Bearer: []

    responses:
      200:
        description: Feed retrieved successfully
      401:
        description: Missing or invalid token
      500:
        description: Internal server error
    """
    try:
        posts = PostService.get_global_feed()
        posts_json = [
            {
                "id": p.id,
                "content": p.content,
                "created_at": p.created_at.isoformat(),
                "author_id": p.author_id,
            } for p in posts 
        ]

        return jsonify(posts_json), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"error": "An internal server error occurred."}), 500
    
@post_bp.route('/following', methods=['GET'])
@jwt_required()
def get_following_feed():
    current_user_id = int(get_jwt_identity())

    try:
        posts = PostService.get_following_feed(current_user_id)

        posts_json = [{
            "id": p.id,
            "content": p.content,
            "created_at": p.created_at.isoformat(),
            "author_id": p.author_id,
            } for p in posts
        ]
        return jsonify(posts_json), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"error": "An internal server error occurred."}), 500
    
    
@post_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    current_user_id = int(get_jwt_identity())

    try:
        user = UserRepository.get_by_id(current_user_id)
        if not user:
            return jsonify({"error": "User not found."}), 404
        
        PostService.delete_post(
            post_id=post_id,
            requesting_user_id=current_user_id,
            requesting_user_role=user.role
        )

        return jsonify({"message": "Post deleted successfully!"}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404 #404 -> Not found
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403 #403 -> Forbidden
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"error": "An internal server error occurred."}), 500
    
@post_bp.route('/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    current_user_id = int(get_jwt_identity())

    try:
        PostService.like_post(
            post_id=post_id,
            user_id=current_user_id
        )
        return jsonify({"message": "You liked this post."}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"error": "An internal server error occurred."}), 500
    
@post_bp.route('/<int:post_id>/dislike', methods=['POST'])
@jwt_required()
def dislike_post(post_id):
    current_user_id = int(get_jwt_identity())

    try:
        PostService.dislike_post(
            post_id=post_id,
            user_id=current_user_id
        )
        return jsonify({"message": "You removed your like from this post."}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        
        return jsonify({"error": "An internal server error occurred."}), 500
    
@post_bp.route('/<int:post_id>/retweet', methods=['POST'])
@jwt_required()
def retweet_post(post_id):
    """
    ---
    tags:
       - Posts
    security:
      - Bearer: []
    parameters:
       - in: path
         name: post_id
         type: integer
         required: true
         description: ID of the post to retweet
    responses:
      200:
        description: Retweet removed successfully (Toggle OFF)
      201:
        description: Retweet added successfully (Toggle ON)
      400:
        description: Validation error
      401:
        description: Missing or invalid token
      500:
        description: Internal server error
    """
    current_user_id = int(get_jwt_identity())

    try:
        result = PostService.retweet_post(original_post_id=post_id, user_id=current_user_id)
        status_code = 201 if result["action"] == "added" else 200
        return jsonify({
            "message": result["message"],
            "action": result["action"]
        }), status_code
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred."}), 500
    
@post_bp.route('/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post_details(post_id):
    current_user_id = int(get_jwt_identity())
    try:
        result = PostService.retweet_post(original_post_id=post_id, user_id=current_user_id)
        status_code = 201 if result["action"] == "added" else 200

        return jsonify({
            "message": result["message"],
            "action": result["action"]
        }), status_code
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred."}), 500
@post_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    """
    ---
    tags:
       - Posts
    security:
      - Bearer: []
    summary: Update any post.
    parameters:
       - in: path
         name: post_id
         type: integer
         required: true
         description: ID of the post to update
       - in: body
         name: body
         required: true
         schema:
           type: object
           properties:
             text:
               type: string
               example: "Updated post content"
    responses:
       200:
        description: Post updated successfully
       400:
        description: Validation error (e.g., empty content)
       403:
        description: Access denied (You're not the author of the post)
       404:
        description: Post not found
       500:
        description: Internal server error
    """
    current_user_id = int(get_jwt_identity())
    data = request.get_json()

    try:
        result = PostService.update_post(
            post_id,
            current_user_id,
            data
        )
        return jsonify(result), 200
    
    except ValueError as e:
        status_code = 404 if "not found" in str(e).lower() else 400
        return jsonify({"error": str(e)}), status_code
    
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred."}), 500