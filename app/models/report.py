from app import db
from datetime import datetime

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)

    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    reported_post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    reported_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    reason = db.Column(db.String(280), nullable=False)

    status = db.Column(db.String(20), default='pending', nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    reporter = db.relationship('User', foreign_keys=[reporter_id], backref=db.backref('reports_made', lazy=True))
    repoted_post = db.relationship('Post', foreign_keys=[reported_post_id], backref=db.backref('reports', lazy=True))
    reported_user = db.relationship('User', foreign_keys=[reported_user_id], backref=db.backref('reports_received', lazy=True))
    reviewed_by = db.relationship('User', foreign_keys=[reviewed_by_id])

    def __repr__(self):
        target = f"Post {self.reported_post_id}" if self.reported_post_id else f"User {self.reported_user_id}"
        return f'<Report {self.id} by User {self.reporter_id} on {target}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "reporter_id": self.reporter_id,
            "reported_post_id": self.reported_post_id,
            "reported_user_id": self.reported_user_id,
            "reason": self.reason,
            "status": self.status,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "reviewed_at": self.reviewed_at.strftime('%Y-%m-%d %H:%M:%S') if self.reviewed_at else None,
            "reviewed_by_id": self.reviewed_by_id,
        }

