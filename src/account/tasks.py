from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from .utility import generate_validation_link
from django.contrib.auth import get_user_model


@shared_task
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

@shared_task
def send_welcoming_email_to_new_users(email):
    subject = "Happy To See you On board!"
    
    # Plain-text version of the email (message)
    message = """
    Hello!

    We’re thrilled to have you on board. Get ready to explore and enjoy all the features we have to offer.

    If you have any questions, feel free to reach out. We’re here to help!

    Best regards,
    The Shinemakers Team
    """
    
    # HTML version of the email
    html_message = f"""
    <html>
    <body>
        <h2>Welcome to Our Community!</h2>
        <p>We’re thrilled to have you on board. Get ready to explore and enjoy all the features we have to offer.</p>
        
        <p>If you have any questions, feel free to reach out. We’re here to help!</p>

        <p>Best regards,</p>
        <p><strong>The Shinemakers Team</strong></p>
    </body>
    </html>
    """
    
    # Sending the email
    send_mail(
        subject=subject,
        message=message,  # Plain text version of the message
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html_message,  # HTML version of the message
    )


@shared_task
def validate_new_user_email(email, token):
    try:
        # Get the user by email
        User = get_user_model()
        user = User.objects.get(email=email)
        # Generate the validation link
        validation_link = generate_validation_link(user, token)
        
        subject = "Email Validation"
        
        html_message = f"""
       <html>
        <body>
            <p>Dear User,</p>
            <p>Thank you for registering with us. To complete your registration, please click the button below to validate your email address:</p>
            <a href="{validation_link}" 
            style="background-color: #007bff; color: white; padding: 10px 20px; 
                    text-decoration: none; border-radius: 5px; display: inline-block;">
            Validate Your Email
            </a>
            <p>If you did not register for this account, please disregard this email.</p>
            <p>Best regards,<br>Your Company Team</p>
        </body>
    </html>  """
        
        plain_message = f"Click the link below to validate your email:\n\n{validation_link}"
        
        # Send the email with both plain and HTML versions
        send_mail(
            subject=subject,
            message=plain_message,  # Fallback for non-HTML email clients
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,  # Sends HTML email
        )
    except User.DoesNotExist:
        # Handle the case where the user with the given email does not exist
        raise ValueError(f"User with email {email} not found.")
    

@shared_task
def send_order_confirmation_email(user_email, user_id, order_id, serialized_order_details, totals, shipping_address):
    print(serialized_order_details)
    # Fetch the user object from the database using the user_id
    User = get_user_model()
    user = User.objects.get(id=user_id)
    
    # Subject of the email
    subject = f"Order Confirmation - Order #{order_id}"

    # Plain-text version of the email (message)
    message = f"""
    Hello {user.first_name},

    Thank you for your order! Your order (Order #{order_id}) has been successfully placed.

    Order Details:
    ---------------------
    Order ID: {order_id}
    Total Cost: ${totals['cart_total']}
    
    Order Summary:
    ---------------------
    """
    
    for detail in serialized_order_details:
        message += f"{detail['product_name']} - {detail['quantity']} x ${detail['cost']} each\n"

    message += f"\nShipping Address: {shipping_address}\n\n"
    message += "You will receive another email once your order has been shipped.\n"
    message += "If you have any questions, feel free to contact us. We’re here to help!\n"
    message += "Thank you for choosing us.\n\n"
    message += f"Best regards,\nThe Shinemakers Team"

    # HTML version of the email
    html_message = f"""
    <html>
    <body>
        Hello {user.first_name},

        Thank you for your order! Your order (Order #{order_id}) has been successfully placed.
        
        <h3>Order Details:</h3>
        <ul>
            <li><strong>Order ID:</strong> {order_id}</li>
            <li><strong>Total Cost:</strong> ${totals['cart_total']}</li>
        </ul>

        <h3>Order Summary:</h3>
        <ul>
    """
    for detail in serialized_order_details:
        html_message += f"<li>{detail['product_name']} - {detail['quantity']} x ${detail['cost']} each</li>"
    
    html_message += f"""
        </ul>
        <p><strong>Shipping Address:</strong> {shipping_address}</p>
        <p>You will receive another email once your order has been shipped.</p>
        <p>If you have any questions, feel free to contact us. We’re here to help!</p>
        <p>Thank you for choosing us.</p>

        <p>Best regards,</p>
        <p><strong>The Shinemakers Team</strong></p>
    </body>
    </html>
    """

    # Sending the email
    send_mail(
        subject=subject,
        message=message,  # Plain text version of the message
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        html_message=html_message,  # HTML version of the message
    )
    
 

