import os
from dotenv import load_dotenv
from flask import Flask, render_template, session, redirect, url_for
from flask_mail import Mail
from models import db
from routes import auth_bp, detection_bp, events_bp
from routes.auth import mail

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME', 'noreply@blurdetect.com')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SERVER_URL'] = os.getenv('SERVER_URL', 'http://localhost:5000')

# Initialize extensions
db.init_app(app)
mail.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(detection_bp, url_prefix='/detection')
app.register_blueprint(events_bp, url_prefix='')

# Create necessary directories
os.makedirs('static/uploads', exist_ok=True)


# Main routes
@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, else login."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))


@app.route('/dashboard')
def dashboard():
    """User dashboard."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session.get('user_id')
    from models import Image, DetectionResult, SystemEvent
    
    # Get statistics
    total_uploads = Image.query.filter_by(user_id=user_id).count()
    total_detections = DetectionResult.query.filter_by(user_id=user_id).count()
    recent_events = SystemEvent.query.filter_by(user_id=user_id).order_by(
        SystemEvent.timestamp.desc()
    ).limit(5).all()
    
    # Get blur type distribution
    blur_types = {}
    if total_detections > 0:
        results = DetectionResult.query.filter_by(user_id=user_id).all()
        for result in results:
            blur_types[result.blur_type] = blur_types.get(result.blur_type, 0) + 1
    
    return render_template(
        'dashboard.html',
        total_uploads=total_uploads,
        total_detections=total_detections,
        recent_events=recent_events,
        blur_types=blur_types
    )


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
