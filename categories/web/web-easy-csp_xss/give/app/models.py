from . import db
from datetime import datetime
import uuid

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), unique=False, nullable=False)

    created_pools = db.relationship("Pool", back_populates='creator', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.name}>'
    

class Pool(db.Model):

    __tablename__ = 'pools'

    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    options_json = db.Column(db.JSON)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)
    
    creator = db.relationship('User', back_populates='created_pools')
    
    def __repr__(self):
        return f'<Poll {self.id}: {self.title}>'