import os
from flask import Flask, render_template
from models import db
from email_utils import mail
from config import config
from routes_auth import auth_bp
from routes_detection import detection_bp
from routes_dashboard import dashboard_bp

# Create Flask app
app = Flask(__name__)

# Load configuration
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config.get(config_name, config['development']))

# Initialize extensions
db.init_app(app)
mail.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(detection_bp)
app.register_blueprint(dashboard_bp)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Create tables
@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()

# Context processors
@app.context_processor
def inject_user():
    from flask import session
    return dict(current_user_id=session.get('user_id'), current_username=session.get('username'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.getenv('PORT', 5000))
    app.run(debug=app.config.get('DEBUG', False), host='0.0.0.0', port=port)
