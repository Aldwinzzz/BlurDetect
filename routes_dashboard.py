from flask import Blueprint, render_template, session, redirect, url_for
from models import db, User, Image, DetectionResult, SystemEvent
from auth_utils import login_required
from sqlalchemy import desc

dashboard_bp = Blueprint('dashboard_bp', __name__)


@dashboard_bp.route('/', methods=['GET'])
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth_bp.login'))


@dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    
    # Statistics
    total_images = Image.query.filter_by(user_id=session['user_id']).count()
    total_detections = DetectionResult.query.filter_by(user_id=session['user_id']).count()
    
    # Blur type statistics
    blur_stats = db.session.query(
        DetectionResult.blur_type,
        db.func.count(DetectionResult.id).label('count')
    ).filter_by(user_id=session['user_id']).group_by(DetectionResult.blur_type).all()
    
    blur_types_dict = {stat[0]: stat[1] for stat in blur_stats}
    
    # Recent images
    recent_images = Image.query.filter_by(user_id=session['user_id']).order_by(
        Image.uploaded_at.desc()
    ).limit(5).all()
    
    recent_data = []
    for img in recent_images:
        result = DetectionResult.query.filter_by(image_id=img.id).first()
        recent_data.append({
            'image': img,
            'result': result
        })
    
    return render_template('dashboard.html',
                         user=user,
                         total_images=total_images,
                         total_detections=total_detections,
                         blur_types=blur_types_dict,
                         recent_images=recent_data)


@dashboard_bp.route('/events', methods=['GET'])
@login_required
def events():
    # Get events (user's own events + system events)
    user_events = SystemEvent.query.filter_by(user_id=session['user_id']).order_by(
        SystemEvent.timestamp.desc()
    ).all()
    
    return render_template('events.html', events=user_events)


@dashboard_bp.route('/system-events', methods=['GET'])
@login_required
def system_events():
    # Get all system events for admin view
    all_events = SystemEvent.query.order_by(SystemEvent.timestamp.desc()).limit(100).all()
    
    return render_template('system_events.html', events=all_events)
