from django.core.mail import send_mail
from django.conf import settings

def send_password_reset_email(email, reset_link):
    subject = "Password Reset Request"
    
    html_message = f"""
    <html>
    <body>
        <h2>Password Reset Request</h2>
        <p>Click the button below to reset your password:</p>
        <a href="{reset_link}" 
           style="background-color: #007bff; color: white; padding: 10px 20px; 
                  text-decoration: none; border-radius: 5px; display: inline-block;">
           Reset Password
        </a>
        <p>If you didn’t request a password reset, you can ignore this email.</p>
    </body>
    </html>
    """
    
    plain_message = f"Click the link below to reset your password:\n\n{reset_link}\n\nIf you didn’t request this, you can ignore this email."

    send_mail(
        subject=subject,
        message=plain_message,  # Fallback for non-HTML email clients
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html_message,  # Sends HTML email
    )
