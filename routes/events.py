from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import SystemEvent, User

events_bp = Blueprint('events', __name__)


def is_logged_in():
    """Check if user is logged in."""
    return 'user_id' in session


@events_bp.before_request
def check_login():
    """Ensure user is logged in."""
    if not is_logged_in():
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))


@events_bp.route('/events', methods=['GET'])
def view_events():
    """View system events for the logged-in user."""
    user_id = session.get('user_id')
    
    # Get all events for this user
    events = SystemEvent.query.filter_by(user_id=user_id).order_by(
        SystemEvent.timestamp.desc()
    ).all()
    
    return render_template('events.html', events=events)
