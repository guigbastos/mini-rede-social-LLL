from app import db
from datetime import datetime

likes_table = db.Table('likes',
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                       db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
                       )

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    original_post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)

    author = db.relationship('User', backref=db.backref('posts', lazy=True))
    original_post = db.relationship('Post', remote_side=[id], backref='retweets')


    likes = db.relationship(
        'User',
        secondary=likes_table,
        backref=db.backref('liked_posts', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<Post {self.id} by User {self.author_id}>'

    def to_dict(self):
        data = {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "author_id": self.author_id,
            "author_name": self.author.username,
            "likes_count": self.likes.count(),
            "is_retweet": self.original_post is not None,
            "original_post": None
        }

        if self.original_post:
            data["original_post"] = {
                "id": self.original_post.id,
                "content": self.original_post.content,
                "author_id": self.original_post.author_id,
                "likes_count": self.original_post.likes.count(),
                "created_at": self.original_post.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        
        return data