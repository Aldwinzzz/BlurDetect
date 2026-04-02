from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from models import db, User, SystemEvent
import hashlib
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


def hash_password(password):
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def send_verification_email(user_email, token):
    """Send verification email to user."""
    try:
        from flask_mail import Mail
        mail = current_app.extensions.get('mail')
        if not mail:
            print("Mail extension not initialized")
            return False
        
        verification_url = f"{current_app.config.get('SERVER_URL', 'http://localhost:5000')}/auth/verify/{token}"
        
        msg = Message(
            'Verify Your BlurDetect Account',
            recipients=[user_email],
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                    <div style="max-width: 600px; margin: 0 auto; background: #f9fafb; padding: 40px; border-radius: 10px;">
                        <h2 style="color: #007BFF; margin-bottom: 20px;">Welcome to BlurDetect!</h2>
                        <p style="color: #333; font-size: 16px;">Thank you for registering. Please verify your email address by clicking the button below:</p>
                        <div style="margin: 30px 0; text-align: center;">
                            <a href="{verification_url}" 
                               style="background-color: #007BFF; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">
                                Verify Email
                            </a>
                        </div>
                        <p style="color: #666; font-size: 14px;">Or copy this link:</p>
                        <p style="color: #007BFF; word-break: break-all; font-size: 13px;">{verification_url}</p>
                        <p style="color: #999; font-size: 13px; margin-top: 20px;">This link expires in 1 hour.</p>
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                        <p style="color: #666; font-size: 13px;">If you did not register for BlurDetect, please ignore this email.</p>
                    </div>
                </body>
            </html>
            """
        )
        mail.send(msg)
        print(f"Verification email sent successfully to {user_email}")
        return True
    except Exception as e:
        print(f"Error sending email to {user_email}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def generate_verification_token(email):
    """Generate a verification token using itsdangerous."""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm-salt')


def confirm_verification_token(token, expiration=3600):
    """Confirm a verification token."""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
        return email
    except Exception as e:
        print(f"Token error: {e}")
        return None


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new user
        hashed_password = hash_password(password)
        new_user = User(username=username, email=email, password=hashed_password, is_verified=False)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            
            # Log registration event
            event = SystemEvent(
                event_type='USER_REGISTERED',
                user_id=new_user.id,
                message=f'User {username} registered successfully',
                details={'email': email}
            )
            db.session.add(event)
            db.session.commit()
            
            # Send verification email
            token = generate_verification_token(email)
            if send_verification_email(email, token):
                flash('Registration successful! Check your email to verify your account.', 'success')
            else:
                flash('Registration successful, but email verification failed. Please contact support.', 'warning')
            
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error during registration: {str(e)}', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html')


@auth_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    """Verify user email."""
    email = confirm_verification_token(token)
    
    if not email:
        flash('Invalid or expired verification link.', 'danger')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.login'))
    
    if user.is_verified:
        flash('Email already verified. Please log in.', 'info')
        return redirect(url_for('auth.login'))
    
    try:
        user.is_verified = True
        db.session.commit()
        
        event = SystemEvent(
            event_type='USER_VERIFIED',
            user_id=user.id,
            message=f'User {user.username} email verified',
            details={'email': email}
        )
        db.session.add(event)
        db.session.commit()
        
        flash('Email verified successfully! You can now log in.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error verifying email: {str(e)}', 'danger')
    
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required.', 'danger')
            event = SystemEvent(
                event_type='LOGIN_FAILED',
                message='Login attempt with missing credentials'
            )
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('Invalid email or password.', 'danger')
            event = SystemEvent(
                event_type='LOGIN_FAILED',
                message=f'Login attempt with non-existent email: {email}'
            )
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('auth.login'))
        
        if not user.is_verified:
            flash('Please verify your email before logging in.', 'warning')
            event = SystemEvent(
                event_type='LOGIN_FAILED',
                user_id=user.id,
                message=f'Login attempt by unverified user: {user.username}'
            )
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('auth.login'))
        
        hashed_password = hash_password(password)
        if user.password != hashed_password:
            flash('Invalid email or password.', 'danger')
            event = SystemEvent(
                event_type='LOGIN_FAILED',
                user_id=user.id,
                message=f'Failed login attempt for user: {user.username}'
            )
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('auth.login'))
        
        # Login successful
        session['user_id'] = user.id
        session['username'] = user.username
        
        event = SystemEvent(
            event_type='USER_LOGIN',
            user_id=user.id,
            message=f'User {user.username} logged in'
        )
        db.session.add(event)
        db.session.commit()
        
        flash(f'Welcome, {user.username}!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """User logout."""
    if 'user_id' in session:
        user_id = session['user_id']
        username = session.get('username', 'Unknown')
        
        event = SystemEvent(
            event_type='USER_LOGOUT',
            user_id=user_id,
            message=f'User {username} logged out'
        )
        db.session.add(event)
        db.session.commit()
    
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
