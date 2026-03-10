from app import db
from app.models.post import Post
from app.models.user import followers_table, User

class PostRepository:
    @staticmethod
    def create(post: Post) -> Post:
        db.session.add(post)
        db.session.commit()
        return post
    
    @staticmethod
    def get_by_id(post_id: int) -> Post:
        return Post.query.get(post_id)
    
    @staticmethod
    def get_all_active() -> list[Post]:
        return Post.query.filter_by(is_active=True).order_by(Post.created_at.desc()).all()
    
    @staticmethod
    def get_by_author_id(author_id: int) -> list[Post]:
        return Post.query.filter_by(author_id=author_id, is_active=True).order_by(Post.created_at.desc()).all()
    
    @staticmethod
    def update(post: Post) -> Post:
        db.session.commit()
        return post
    
    @staticmethod
    def delete(post: Post) -> None:
        db.session.delete(post)
        db.session.commit()

    @staticmethod
    def get_following_feed(user_id: int) -> list[Post]:
        followed_ids = db.session.query(followers_table.c.followed_id).filter(followers_table.c.follower_id == user_id)

        return Post.query.filter(
            Post.author_id.in_(followed_ids),
            Post.is_active == True
        ).order_by(
            Post.created_at.desc()
        ).all()

    @staticmethod
    def is_liked_by(post: Post, user: User) -> bool:
        return post.likes.filter_by(id=user.id).first() is not None
    
    @staticmethod
    def like(post: Post, user: User) -> None:
        if not PostRepository.is_liked_by(post, user):
            post.likes.append(user)
            db.session.commit()

    @staticmethod
    def unlike(post: Post, user: User) -> None:
        if PostRepository.is_liked_by(post, user):
            post.likes.remove(user)
            db.session.commit()
