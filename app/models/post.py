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

    author = db.relationship('User', backref=db.backref('posts', lazy=True))

    likes = db.relationship(
        'User',
        secondary=likes_table,
        backref=db.backref('liked_posts', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<Post {self.id} by User {self.author_id}>'