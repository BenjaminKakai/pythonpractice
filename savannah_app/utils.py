from django.conf import settings
from django.core.mail import send_mail
import africastalking

def send_sms(phone_number, message):
    africastalking.initialize(
        username=settings.AT_USERNAME,
        api_key=settings.AT_API_KEY
    )
    sms = africastalking.SMS
    try:
        response = sms.send(message=message, recipients=[phone_number])
        return response
    except Exception as e:
        print(f"SMS sending failed: {str(e)}")
        return None

def send_order_notification(order):
    # Send SMS to customer
    sms_message = f"Your order #{order.id} has been placed successfully!"
    send_sms(order.customer.phone, sms_message)
    
    # Send email to admin
    send_mail(
        subject=f'New Order #{order.id}',
        message=f'Order details: {order}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
    )