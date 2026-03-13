from app import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    author = db.relationship('User', backref=db.backref('comments', lazy=True))
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f'<Comment {self.id} on Post {self.post_id} by User {self.author_id}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "author_id": self.author_id,
            "author_name": self.author.username,
            "post_id": self.post_id
        }