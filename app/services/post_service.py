from app.models.post import Post
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository

class PostService:
    @staticmethod
    def create_post(author_id: int, content: str) -> Post:
        if not content or not content.strip():
            raise ValueError("O conteúdo da postagem não pode ser vazio.")
        
        if len(content) > 280:
            raise ValueError("A postagem ultrapassa o limite de caracteres (280).")
        
        author = UserRepository.get_by_id(author_id)

        if not author.is_active:
            raise ValueError("O autor da postagem não está ativo.")
        
        new_post = Post(
            content=content.strip(),
            author_id=author_id
        )

        return PostRepository.create(new_post)
    
    @staticmethod
    def get_global_feed() -> list[Post]:
        return PostRepository.get_all_active()
    
    @staticmethod
    def delete_post(post_id: int, requesting_user_id: int, requesting_user_role: str) -> None:
        post = PostRepository.get_by_id(post_id)

        if not post or not post.is_active:
            raise ValueError("Postagem não foi encontrada ou foi removida.")
        
        if post.author_id != requesting_user_id and requesting_user_role not in ['admin', 'moderator']:
            raise ValueError("Você não tem permissão para excluir esta postagem.")
        
        post.is_active = False
        PostRepository.update(post)
    
    @staticmethod
    def get_following_feed(user_id: int) -> list[Post]:
        return PostRepository.get_following_feed(user_id)
    
    @staticmethod
    def like_post(post_id: int, user_id: int) -> None:
        user = UserRepository.get_by_id(user_id)
        post = PostRepository.get_by_id(post_id)

        if not user:
            raise ValueError("Usuário não encontrado.")
        
        if not post:
            raise ValueError("Postagem não encontrada ou removida.")

        if PostRepository.is_liked_by(post, user):
            raise ValueError("Você já curtiu esta postagem.")
        
        PostRepository.like(post, user)

    @staticmethod
    def dislike_post(post_id: int, user_id: int) -> None:
        user = UserRepository.get_by_id(user_id)
        post = PostRepository.get_by_id(post_id)

        if not user:
            raise ValueError("Usuário não encontrado.")
        
        if not post or not post.is_active:
            raise ValueError("Postagem não encontrada ou removida.")
        
        if not PostRepository.is_liked_by(post, user):
            raise ValueError("Você não curtiu esta postagem para poder descurtir.")
        
        PostRepository.unlike(post, user)

    @staticmethod
    def retweet_post(original_post_id: id, user_id: int) -> None:
        user = UserRepository.get_by_id(user_id)
        original_post = PostRepository.get_by_id(original_post_id)

        if not user:
            raise ValueError("Usuário não encontrado.")
        
        if not original_post or not original_post.is_active:
            raise ValueError("Postagem original não encontrada ou removida.")
        
        existing_retweet = PostRepository.get_user_retweet(original_post_id, user_id)

        if existing_retweet:
            existing_retweet.is_active = False

            PostRepository.save(existing_retweet)
            return {"acao": "removido", "mensagem": "Retweet desfeito com succeso!"}
        else:
            from app.models.post import Post
            novo_retweet = Post(
                content="",
                author_id=user_id,
                original_post_id=original_post.id
            )
            PostRepository.save(novo_retweet)
            return {"acao": "adicionado", "mensagem": "Retweet feito com succeso!"}



        