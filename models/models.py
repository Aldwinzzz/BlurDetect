from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    images = db.relationship('Image', backref='user', lazy=True, cascade='all, delete-orphan')
    detection_results = db.relationship('DetectionResult', backref='user', lazy=True, cascade='all, delete-orphan')
    system_events = db.relationship('SystemEvent', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class Image(db.Model):
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    filename = db.Column(db.Text, nullable=False)
    upload_path = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    detection_results = db.relationship('DetectionResult', backref='image', lazy=True, cascade='all, delete-orphan')
    model_comparisons = db.relationship('ModelComparison', backref='image', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Image {self.filename}>'


class DetectionResult(db.Model):
    __tablename__ = 'detection_results'
    
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    model_used = db.Column(db.Text, nullable=False)
    blur_type = db.Column(db.Text, nullable=False)  # 'Gaussian', 'Motion', 'Defocus', 'Lens', 'Sharp'
    confidence = db.Column(db.Float)
    blur_score = db.Column(db.Float)
    explanation = db.Column(db.Text)
    processing_time = db.Column(db.Float)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DetectionResult {self.blur_type}>'


class ModelComparison(db.Model):
    __tablename__ = 'model_comparisons'
    
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id', ondelete='CASCADE'), nullable=False)
    model_name = db.Column(db.Text, nullable=False)
    blur_type = db.Column(db.Text, nullable=False)
    confidence = db.Column(db.Float)
    processing_time = db.Column(db.Float)
    ran_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ModelComparison {self.model_name}>'


class SystemEvent(db.Model):
    __tablename__ = 'system_events'
    
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    message = db.Column(db.Text)
    details = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SystemEvent {self.event_type}>'
