"""
Email verification utility functions for user registration
"""
import secrets
import os
from datetime import datetime, timedelta
from flask import url_for, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import db
from models import User
from i18n import _


def generate_verification_token():
    """Generate a secure verification token"""
    return secrets.token_urlsafe(32)


def send_verification_email(user, token):
    """Send email verification email to user using SendGrid"""
    try:
        # Check if SendGrid API key is available
        sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
        if not sendgrid_api_key:
            print("Warning: SENDGRID_API_KEY not found. Email verification disabled.")
            return False
        
        # Create verification URL
        verification_url = url_for('verify_email', token=token, _external=True)
        
        # Email content
        subject = "驗證您的 464955 帳戶 / Verify Your 464955 Account"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Email Verification</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .logo {{ font-size: 24px; font-weight: bold; color: #0d6efd; margin-bottom: 10px; }}
                .title {{ font-size: 20px; margin-bottom: 20px; color: #333; }}
                .content {{ line-height: 1.6; color: #666; }}
                .button {{ display: inline-block; padding: 12px 30px; background-color: #0d6efd; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; }}
                .warning {{ background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 15px; margin: 20px 0; color: #856404; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">464955</div>
                    <div class="title">歡迎加入 464955！/ Welcome to 464955!</div>
                </div>
                
                <div class="content">
                    <p><strong>中文：</strong></p>
                    <p>感謝您註冊 464955 行銷媒合平台！</p>
                    <p>請點擊下方按鈕驗證您的電子郵件地址以完成註冊：</p>
                    
                    <div style="text-align: center;">
                        <a href="{verification_url}" class="button">驗證電子郵件</a>
                    </div>
                    
                    <div class="warning">
                        <strong>重要提醒：</strong>此驗證連結將在 24 小時後過期，請盡快完成驗證。
                    </div>
                    
                    <hr style="margin: 30px 0;">
                    
                    <p><strong>English:</strong></p>
                    <p>Thank you for registering with 464955 marketing platform!</p>
                    <p>Please click the button below to verify your email address and complete registration:</p>
                    
                    <div style="text-align: center;">
                        <a href="{verification_url}" class="button">Verify Email</a>
                    </div>
                    
                    <div class="warning">
                        <strong>Important:</strong> This verification link will expire in 24 hours. Please verify as soon as possible.
                    </div>
                    
                    <p style="margin-top: 30px;">如果按鈕無法點擊，請複製以下連結到瀏覽器：<br>
                    If the button doesn't work, copy this link to your browser:</p>
                    <p style="word-break: break-all; color: #0d6efd;">{verification_url}</p>
                </div>
                
                <div class="footer">
                    <p>此郵件由 464955 系統自動發送，請勿直接回覆。<br>
                    This email was sent automatically by 464955 system. Please do not reply directly.</p>
                    <p>© 2024 464955. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        歡迎加入 464955！/ Welcome to 464955!
        
        中文：
        感謝您註冊 464955 行銷媒合平台！
        請前往以下連結驗證您的電子郵件地址：
        {verification_url}
        
        重要：此驗證連結將在 24 小時後過期。
        
        English:
        Thank you for registering with 464955 marketing platform!
        Please visit the following link to verify your email address:
        {verification_url}
        
        Important: This verification link will expire in 24 hours.
        
        © 2024 464955. All rights reserved.
        """
        
        # Send email using SendGrid
        sg = SendGridAPIClient(api_key=sendgrid_api_key)
        
        message = Mail(
            from_email='noreply@464955.xyz',
            to_emails=user.email,
            subject=subject,
            html_content=html_content,
            plain_text_content=text_content
        )
        
        response = sg.send(message)
        print(f"Email verification sent to {user.email}. SendGrid response: {response.status_code}")
        return True
        
    except Exception as e:
        print(f"Email sending error: {str(e)}")
        return False


def create_verification_token(user):
    """Create and store verification token for user"""
    token = generate_verification_token()
    user.email_verification_token = token
    user.email_verification_sent_at = datetime.utcnow()
    db.session.commit()
    return token


def verify_token(token):
    """Verify email verification token"""
    if not token:
        return None, "無效的驗證連結"
    
    user = User.query.filter_by(email_verification_token=token).first()
    if not user:
        return None, "無效的驗證連結"
    
    # Check if token is expired (24 hours)
    if user.email_verification_sent_at:
        expiry_time = user.email_verification_sent_at + timedelta(hours=24)
        if datetime.utcnow() > expiry_time:
            return None, "驗證連結已過期，請重新申請驗證郵件"
    
    return user, None


def mark_email_verified(user):
    """Mark user's email as verified and clear verification token"""
    user.email_verified = True
    user.email_verification_token = None
    user.email_verification_sent_at = None
    db.session.commit()


def resend_verification_email(user):
    """Resend verification email to user"""
    # Check if user already verified
    if user.email_verified:
        return False, _('email_already_verified')
    
    # Check rate limiting (prevent spam - max 1 email per 5 minutes)
    if user.email_verification_sent_at:
        time_since_last = datetime.utcnow() - user.email_verification_sent_at
        if time_since_last < timedelta(minutes=5):
            remaining_minutes = 5 - int(time_since_last.total_seconds() / 60)
            return False, f"請等待 {remaining_minutes} 分鐘後再重新發送驗證郵件"
    
    # Create new token and send email
    token = create_verification_token(user)
    success = send_verification_email(user, token)
    
    if success:
        return True, _('verification_email_sent')
    else:
        return False, _('verification_email_error')