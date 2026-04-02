from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from models import db, User, SystemEvent
from auth_utils import hash_password, verify_password, generate_verification_token, login_required
from email_utils import send_verification_email
from datetime import datetime

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('auth_bp.register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('auth_bp.register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth_bp.register'))
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth_bp.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth_bp.register'))
        
        # Create user
        verification_token = generate_verification_token()
        user = User(
            username=username,
            email=email,
            password=hash_password(password),
            verification_token=verification_token,
            email_verified=False
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Log event
        event = SystemEvent(
            event_type='USER_REGISTERED',
            user_id=user.id,
            message=f'User {username} registered successfully'
        )
        db.session.add(event)
        db.session.commit()
        
        # Send verification email
        send_verification_email(email, verification_token)
        
        flash('Registration successful! Please check your email to verify your account.', 'success')
        return redirect(url_for('auth_bp.login'))
    
    return render_template('register.html')


@auth_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    user = User.query.filter_by(verification_token=token).first()
    
    if not user:
        flash('Invalid or expired verification link.', 'danger')
        return redirect(url_for('auth_bp.login'))
    
    user.email_verified = True
    user.verification_token = None
    db.session.commit()
    
    flash('Email verified successfully! You can now log in.', 'success')
    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('auth_bp.login'))
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not verify_password(password, user.password):
            # Log failed login attempt
            event = SystemEvent(
                event_type='LOGIN_FAILED',
                message=f'Failed login attempt for username: {username}'
            )
            db.session.add(event)
            db.session.commit()
            
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('auth_bp.login'))
        
        if not user.email_verified:
            flash('Please verify your email before logging in.', 'warning')
            return redirect(url_for('auth_bp.login'))
        
        # Successful login
        session['user_id'] = user.id
        session['username'] = user.username
        session['email'] = user.email
        
        # Log event
        event = SystemEvent(
            event_type='USER_LOGIN',
            user_id=user.id,
            message=f'User {username} logged in successfully'
        )
        db.session.add(event)
        db.session.commit()
        
        flash(f'Welcome back, {username}!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    user_id = session.get('user_id')
    username = session.get('username')
    
    # Log event
    event = SystemEvent(
        event_type='USER_LOGOUT',
        user_id=user_id,
        message=f'User {username} logged out'
    )
    db.session.add(event)
    db.session.commit()
    
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth_bp.login'))
    
    return render_template('profile.html', user=user)
