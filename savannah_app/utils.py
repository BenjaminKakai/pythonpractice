from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
import africastalking

def initialize_africastalking():
    """Initialize Africa's Talking SMS gateway."""
    africastalking.initialize(
        username=settings.AT_USERNAME,
        api_key=settings.AT_API_KEY
    )
    return africastalking.SMS

def send_sms(phone_number, message):
    """Send SMS using Africa's Talking gateway."""
    sms = initialize_africastalking()
    try:
        response = sms.send(message=message, recipients=[phone_number])
        return response
    except Exception as e:
        print(f"SMS sending failed: {str(e)}")
        return None

def send_admin_email(subject, message_content):
    """Send email notification to administrators."""
    try:
        send_mail(
            subject=subject,
            message=message_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        return False

def send_order_notification(order):
    """Send notifications for new orders and status updates."""
    # SMS notification to customer
    status_messages = {
        'pending': 'is pending confirmation',
        'processing': 'is being processed',
        'shipped': 'has been shipped',
        'delivered': 'has been delivered',
        'cancelled': 'has been cancelled'
    }
    
    status_msg = status_messages.get(order.status, 'status has been updated')
    sms_message = f"Order #{order.order_number} {status_msg}. "
    
    if order.status == 'shipped':
        sms_message += f"Track your order with number: {order.order_number}"
    elif order.status == 'delivered':
        sms_message += "Thank you for shopping with us!"
    
    send_sms(order.customer.phone, sms_message)
    
    # Email notification to admin
    subject = f'Order #{order.order_number} - {order.status.title()}'
    
    # Detailed order information for admin
    message_content = f"""
Order Details:
-------------
Order Number: {order.order_number}
Status: {order.status}
Customer: {order.customer.user.username}
Phone: {order.customer.phone}
Total Amount: ${order.total_amount}
Shipping Address: {order.shipping_address}
Date: {order.created_at}

Items:
------
"""
    for item in order.items.all():
        message_content += f"- {item.quantity}x {item.product.name} @ ${item.price} each\n"
    
    send_admin_email(subject, message_content)

def send_order_confirmation(order):
    """Send initial order confirmation notifications."""
    # SMS to customer
    sms_message = (
        f"Thank you for your order #{order.order_number}! "
        f"Total amount: ${order.total_amount}. "
        "We'll notify you when your order is processed."
    )
    send_sms(order.customer.phone, sms_message)
    
    # Email to admin
    subject = f'New Order #{order.order_number} Received'
    message_content = f"""
New Order Received!
------------------
Order Number: {order.order_number}
Customer: {order.customer.user.username}
Phone: {order.customer.phone}
Total Amount: ${order.total_amount}
Shipping Address: {order.shipping_address}
Date: {order.created_at}

Items:
------
"""
    for item in order.items.all():
        message_content += f"- {item.quantity}x {item.product.name} @ ${item.price} each\n"
    
    message_content += "\nPlease process this order as soon as possible."
    
    send_admin_email(subject, message_content)