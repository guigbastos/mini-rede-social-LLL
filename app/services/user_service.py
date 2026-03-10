from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def create_user(username: str, email: str, password: str) -> User:
        if UserRepository.get_by_email(email):
            raise ValueError("Este e-mail já está em uso.")
        
        if UserRepository.get_by_username(username):
            raise ValueError("Este nome de usuário já está em uso.")
        
        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            role="user"
        )

        return UserRepository.create(new_user)
    
    @staticmethod
    def authenticate(email: str, password: str) -> User:
        user = UserRepository.get_by_email(email)

        if not user or not check_password_hash(user.password_hash, password):
            return None
        
        return user
    
    @staticmethod
    def follow_user(follower_id: int, followed_id: int) -> None:
        if follower_id == followed_id:
            raise ValueError("Você não pode seguir a si mesmo.")
        
        follower = UserRepository.get_by_id(follower_id)
        followed = UserRepository.get_by_id(followed_id)

        if not follower or not followed:
            raise ValueError("Usuário não encontrado.")
        
        if UserRepository.is_following(follower, followed):
            raise ValueError("Você já está seguindo este usuário.")
        
        UserRepository.follow(follower, followed)

    @staticmethod
    def unfollow_user(follower_id: int, followed_id: int) -> None:
        if follower_id == followed_id:
            raise ValueError("Você não pode deixar de seguir a si mesmo.")
        
        follower = UserRepository.get_by_id(follower_id)
        followed = UserRepository.get_by_id(followed_id)

        if not follower or not followed:
            raise ValueError("Usuário não encontrado.")

        if UserRepository.is_following(follower, followed):
            raise ValueError("Você não está seguindo este usuário.")
        
        UserRepository.unfollow(follower, followed)


