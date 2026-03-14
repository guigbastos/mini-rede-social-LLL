from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.comment_service import CommentService

comment_bp = Blueprint('comment_bp', __name__)

@comment_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    current_user_id = int(get_jwt_identity())
    data = request.get_json()

    content = data.get('content', '')

    try:
        new_comment = CommentService.create_comment(
            content=content,
            user_id=current_user_id,
            post_id=post_id
        )

        return jsonify({"message": "Comment created successfully!", "comment": new_comment.to_dict()}), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred."}), 500
    
@comment_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
@jwt_required()
def get_comments(post_id):
    try:
        comments = CommentService.get_comments_by_post(post_id)

        comments_json = [comment.to_dict() for comment in comments]

        return jsonify(comments_json), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"error": "An internal server error occurred."}), 500
    
