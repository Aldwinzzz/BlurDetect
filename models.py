from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(255), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    images = db.relationship('Image', backref='user', lazy=True, cascade='all, delete-orphan')
    events = db.relationship('SystemEvent', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class Image(db.Model):
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    upload_path = db.Column(db.String(512), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    detection_results = db.relationship('DetectionResult', backref='image', lazy=True, cascade='all, delete-orphan')
    model_comparisons = db.relationship('ModelComparison', backref='image', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Image {self.filename}>'


class DetectionResult(db.Model):
    __tablename__ = 'detection_results'
    
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    model_used = db.Column(db.String(120), nullable=False)
    blur_type = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float)
    blur_score = db.Column(db.Float)
    explanation = db.Column(db.Text)
    processing_time = db.Column(db.Float)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='detection_results')
    
    def __repr__(self):
        return f'<DetectionResult {self.blur_type}>'


class ModelComparison(db.Model):
    __tablename__ = 'model_comparisons'
    
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    model_name = db.Column(db.String(120), nullable=False)
    blur_type = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float)
    processing_time = db.Column(db.Float)
    ran_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ModelComparison {self.model_name}>'


class SystemEvent(db.Model):
    __tablename__ = 'system_events'
    
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text)
    details = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SystemEvent {self.event_type}>'
