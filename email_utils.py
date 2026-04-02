from flask_mail import Mail, Message
from flask import url_for

mail = Mail()


def send_verification_email(user_email: str, verification_token: str, app=None):
    """Send email verification link to user"""
    try:
        verification_url = url_for('auth_bp.verify_email', token=verification_token, _external=True)
        
        msg = Message(
            subject='BlurDetect - Verify Your Email',
            recipients=[user_email],
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 8px; color: white; text-align: center;">
                            <h1>BlurDetect</h1>
                            <p>Welcome to BlurDetect - Your Blur Type Detection Platform</p>
                        </div>
                        
                        <div style="padding: 30px; background: #f9f9f9; margin-top: 20px; border-radius: 8px;">
                            <h2>Verify Your Email Address</h2>
                            <p>Thank you for signing up! To complete your registration, please verify your email address by clicking the button below:</p>
                            
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="{verification_url}" style="background: #667eea; color: white; padding: 12px 30px; border-radius: 6px; text-decoration: none; display: inline-block; font-weight: bold;">
                                    Verify Email Address
                                </a>
                            </div>
                            
                            <p style="color: #666; font-size: 12px; margin-top: 20px;">
                                Or copy this link: <br>
                                <code>{verification_url}</code>
                            </p>
                            
                            <p style="color: #666; margin-top: 20px;">
                                This link will expire in 24 hours.
                            </p>
                        </div>
                        
                        <div style="text-align: center; margin-top: 30px; color: #999; font-size: 12px;">
                            <p>If you did not create this account, please ignore this email.</p>
                            <p>&copy; 2024 BlurDetect. All rights reserved.</p>
                        </div>
                    </div>
                </body>
            </html>
            """
        )
        
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def send_password_reset_email(user_email: str, reset_token: str, app=None):
    """Send password reset email"""
    try:
        reset_url = url_for('auth_bp.reset_password', token=reset_token, _external=True)
        
        msg = Message(
            subject='BlurDetect - Password Reset Request',
            recipients=[user_email],
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 8px; color: white; text-align: center;">
                            <h1>BlurDetect</h1>
                            <p>Password Reset Request</p>
                        </div>
                        
                        <div style="padding: 30px; background: #f9f9f9; margin-top: 20px; border-radius: 8px;">
                            <h2>Reset Your Password</h2>
                            <p>You requested a password reset. Click the button below to reset your password:</p>
                            
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="{reset_url}" style="background: #667eea; color: white; padding: 12px 30px; border-radius: 6px; text-decoration: none; display: inline-block; font-weight: bold;">
                                    Reset Password
                                </a>
                            </div>
                            
                            <p style="color: #666; font-size: 12px; margin-top: 20px;">
                                Or copy this link: <br>
                                <code>{reset_url}</code>
                            </p>
                            
                            <p style="color: #666; margin-top: 20px;">
                                This link will expire in 1 hour.
                            </p>
                        </div>
                        
                        <div style="text-align: center; margin-top: 30px; color: #999; font-size: 12px;">
                            <p>If you did not request this reset, please ignore this email.</p>
                            <p>&copy; 2024 BlurDetect. All rights reserved.</p>
                        </div>
                    </div>
                </body>
            </html>
            """
        )
        
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
