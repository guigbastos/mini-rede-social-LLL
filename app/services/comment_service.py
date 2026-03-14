from app.repositories.comment_repository import CommentRepository
from app.repositories.post_repository import PostRepository
from app.models.comment import Comment

class CommentService:
    @staticmethod
    def create_comment(content: str, user_id: int, post_id: int) -> Comment:
        if not content or not content.strip():
            raise ValueError("Comments shouldn't be empty.")
        
        post = PostRepository.get_by_id(post_id)
        if not post or not post.is_active:
            raise ValueError("Original post not found or removed.")
        
        new_comment = Comment(
            content=content.strip(),
            author_id=user_id,
            post_id=post_id
        )

        CommentRepository.create(new_comment)
        return new_comment
    
    @staticmethod
    def get_comments_by_post(post_id: int) -> list:
        post = PostRepository.get_by_id(post_id)
        if not post or not post.is_active:
            raise ValueError("Post not found or removed.")
        
        return CommentRepository.get_by_post_id(post_id)