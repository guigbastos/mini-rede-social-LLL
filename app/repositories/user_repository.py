from app import db
from app.models.user import User

class UserRepository:

    @staticmethod
    def create(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update(user: User) -> User:
        db.session.commit()
        return user
    
    @staticmethod
    def get_by_id(user_id: int) -> User:
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str) -> User:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_username(username: str) -> User:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def delete(user: User) -> None:
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def is_following(follower: User, followed: User) -> bool:
        return follower.followed.filter_by(id=followed.id).first() is not None

    @staticmethod
    def get_users() -> list:
        return User.query.all()