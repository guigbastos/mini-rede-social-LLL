from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.post_service import PostService
from app.repositories.user_repository import UserRepository

post_bp = Blueprint('posts', __name__, url_prefix='/posts')

@post_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()

    current_user_id = get_jwt_identity()

    if not data or not data.get('content'):
        return jsonify({"Erro": "A postagem não pode ser vazia."})
    
    try: 
        new_post = PostService.create_post(
            author_id=current_user_id,
            content=data['content']
        )
        return jsonify({
            "mensagem": "Postagem criada com sucesso!",
            "id": new_post.id,
            "content": new_post.content,
            "created_at": new_post.created_at.isoformat(),
            "author_id": new_post.author_id,
        }), 201
    except ValueError as e:
        return jsonify({"Erro": str(e)}), 400
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"Erro": "Ocorreu um erro interno no servidor."}), 500
    
@post_bp.route('/', methods=['GET'])
@jwt_required()
def get_feed():
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

        return jsonify({"Erro": "Ocorreu um erro interno no servidor."}), 500
    
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

        return jsonify({"Erro": "Ocorreu um erro interno no servidor."}), 500
    
    
@post_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    current_user_id = int(get_jwt_identity())

    try:
        user = UserRepository.get_by_id(current_user_id)
        if not user:
            return jsonify({"Erro": "Usuário não encontrado."}), 404
        
        PostService.delete_post(
            post_id=post_id,
            requesting_user_id=current_user_id,
            requesting_user_role=user.role
        )

        return jsonify({"mensagem": "Postagem excluída com sucesso!"}), 200
    
    except ValueError as e:
        return jsonify({"Erro": str(e)}), 404 #404 -> Not found
    except PermissionError as e:
        return jsonify({"Erro": str(e)}), 403 #403 -> Forbidden
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"Erro": "Ocorreu um erro interno no servidor."}), 500
    
@post_bp.route('/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    current_user_id = int(get_jwt_identity())

    try:
        PostService.like_post(
            post_id=post_id,
            user_id=current_user_id
        )
        return jsonify({"mensagem": "Você curtiu esta postagem."}), 200
    
    except ValueError as e:
        return jsonify({"Erro": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"Erro": "Ocorreu um erro interno no servidor."}), 500
    
@post_bp.route('/<int:post_id>/dislike', methods=['POST'])
@jwt_required
def dislike_post(post_id):
    current_user_id = int(get_jwt_identity())

    try:
        PostService.dislike_post(
            post_id=post_id,
            user_id=current_user_id
        )
        return jsonify({"mensagem": "Você descurtiu esta postagem."}), 200
    
    except ValueError as e:
        return jsonify({"Erro": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        
        return jsonify({"Erro": "Ocorreu um erro interno no servidor."}), 500
    

    