from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def create_user(username: str, email: str, password: str) -> User:
        if UserRepository.get_by_email(email):
            raise ValueError("This email is already in use.")
        
        if UserRepository.get_by_username(username):
            raise ValueError("This username is already in use.")
        
        if len(password) < 6:
            raise ValueError("Password must have at least 6 characters.")
        
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
            raise ValueError("You can't follow yourself.")
        
        follower = UserRepository.get_by_id(follower_id)
        followed = UserRepository.get_by_id(followed_id)

        if not follower or not followed:
            raise ValueError("User not found.")
        
        if UserRepository.is_following(follower, followed):
            raise ValueError("You are already following this user.")
        
        UserRepository.follow(follower, followed)

    @staticmethod
    def unfollow_user(follower_id: int, followed_id: int) -> None:
        if follower_id == followed_id:
            raise ValueError("You can't unfollow yourself.")
        
        follower = UserRepository.get_by_id(follower_id)
        followed = UserRepository.get_by_id(followed_id)

        if not follower or not followed:
            raise ValueError("User not found.")

        if not UserRepository.is_following(follower, followed):
            raise ValueError("You are not following this user.")
        
        UserRepository.unfollow(follower, followed)

    @staticmethod
    def promote_user(target_user_id: int, requester_id: int) -> dict:
        requester = UserRepository.get_by_id(requester_id)
        target_user = UserRepository.get_by_id(target_user_id)

        if not requester or requester.role != 'admin':
            raise ValueError("Only admins can promote users.")

        if not target_user:
            raise ValueError("User not found.")

        if target_user.role == 'moderator':
            raise ValueError("User is already a moderator.")

        target_user.role = 'moderator'
        UserRepository.update(target_user)

        return {"message": f"User {target_user.username} has been promoted to moderator"}
    
    @staticmethod
    def demote_user(target_user_id: int, requester_id: int) -> dict:
        requester = UserRepository.get_by_id(requester_id)
        target_user = UserRepository.get_by_id(target_user_id)

        if not requester or requester.role != 'admin':
            raise ValueError("Only admins can demote users.")
        
        if not target_user:
            raise ValueError("User not found.")
        
        if target_user.role == 'user':
            raise ValueError("User is already a user.")
        
        if target_user.role == 'admin':
            raise ValueError("You can't demote an admin.")
        
        target_user.role = 'user'
        UserRepository.update(target_user)

        return {"message": f"User {target_user.username} has been demoted to user"}
    
    @staticmethod
    def toggle_user_block(target_user_id: int, requester_id: int) -> dict:
        requester = UserRepository.get_by_id(requester_id)
        target_user = UserRepository.get_by_id(target_user_id)

        if not requester or requester.role not in ['admin', 'moderator']:
            raise PermissionError("Access denied! Only moderators and admins can block users.")
        
        if not target_user:
            raise ValueError("User not found.")
        
        if requester.role == 'moderator' and target_user.role == 'admin':
            raise ValueError("You can't block an admin.")
        
        if target_user.is_blocked:
            target_user.is_blocked = False
            target_user.blocked_at = None
            action = "unblocked"
        else:
            target_user.is_blocked = True
            target_user.blocked_at = None
            action = "blocked"

        UserRepository.update(target_user)

        return {"message": f"User {target_user.username} has been {action}."}
    
    @staticmethod
    def get_user_profile(target_user_id: int) -> dict:
        user = UserRepository.get_by_id(target_user_id)

        if not user:
            raise ValueError("User not found.")
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_blocked": user.is_blocked,
            "followers_count": user.followers.count(),
            "following_count": user.followed.count(),
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    @staticmethod
    def get_followers(user_id: int) -> list:
        user = UserRepository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found.")
        
        followers = user.followers.all()
        return [{
            "id": follower.id,
            "username": follower.username,
            "role": follower.role
            } for follower in followers
            ]
    @staticmethod
    def get_following(user_id: int) -> list:
        user = UserRepository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found.")
        
        following = user.followed.all()

        return [{
            "id": followed.id,
            "username": followed.username,
            "role": followed.role
            } for followed in following
            ]
    
    @staticmethod
    def get_all_users(requester_id: int) -> list:
        requester = UserRepository.get_by_id(requester_id)

        if not requester or requester.role != 'admin':
            raise PermissionError("Access denied! Only admins can view all users.")
        
        users = UserRepository.get_users()

        return[{
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "is_blocked": user.is_blocked,
        } for user in users]
    
    @staticmethod
    def admin_update_user(target_user_id: int, requester_id: int, data: dict) -> dict:
        requester = UserRepository.get_by_id(requester_id)
        target_user = UserRepository.get_by_id(target_user_id)

        if not requester or requester.role != 'admin':
            raise PermissionError("Access denied! Only admins can update users.")
        
        if not target_user:
            raise ValueError("User not found.")
        
        if 'username' in data:
            target_user.username = data['username']

        if 'email' in data:
            target_user.email = data['email']

        UserRepository.update(target_user)

        return {"message": f"User {target_user.username} has been updated."}
    
    @staticmethod
    def admin_delete_user(target_user_id: int, requester_id: int) -> dict:
        requester = UserRepository.get_by_id(requester_id)
        target_user = UserRepository.get_by_id(target_user_id)

        if not requester or requester.role != 'admin':
            raise PermissionError("Access denied! Only admins can delete users.")
        
        if not target_user:
            raise ValueError("User not found.")
        
        if target_user.role == 'admin':
            raise ValueError("You can't delete an admin.")
        
        target_user.is_active = False
        UserRepository.update(target_user)

        return {"message": f"User {target_user.username} has been deactivated."}

    @staticmethod
    def admin_reactivate_user(target_user_id: int, requester_id: int) -> dict:
        requester = UserRepository.get_by_id(requester_id)
        target_user = UserRepository.get_by_id(target_user_id)

        if not requester or requester.role != 'admin':
            raise PermissionError("Access denied! Only admins can reactivate users.")

        
        if not target_user:
            raise ValueError("User not found.")
        
        target_user.is_active = True
        UserRepository.update(target_user)

        return {"message": f"User {target_user.username} has been reactivated."}