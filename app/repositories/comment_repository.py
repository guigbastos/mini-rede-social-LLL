from app import db
from app.models.comment import Comment

class CommentRepository:
    @staticmethod
    def create(comment: Comment) -> None:
        db.session.add(comment)
        db.session.commit()

    @staticmethod
    def get_by_post_id(post_id: int) -> list[Comment]:
        return Comment.query.filter_by(post_id=post_id, is_active=True).order_by(Comment.created_at.asc()).all()

    @staticmethod
    def update(comment: Comment) -> Comment:
        db.session.commit()
        return comment

    @staticmethod
    def delete(comment: Comment) -> None:
        comment.is_active = False
        db.session.commit()
