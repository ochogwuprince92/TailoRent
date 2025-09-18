"""
Celery tasks for profiles app.
"""

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from twilio.rest import Client
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_verification_email(user_id, verification_url):
    """Send email verification to user."""
    try:
        from .models import User

        user = User.objects.get(id=user_id)

        subject = "Verify Your TailoRent Account"
        message = f"""
        Hi {user.first_name or 'there'},
        
        Welcome to TailoRent! Please click the link below to verify your email address:
        
        {verification_url}
        
        If you didn't create an account with us, please ignore this email.
        
        Best regards,
        The TailoRent Team
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        logger.info(f"Verification email sent to {user.email}")
        return f"Verification email sent to {user.email}"

    except Exception as e:
        logger.error(f"Failed to send verification email: {str(e)}")
        raise


@shared_task
def send_otp_sms(phone_number, otp_code):
    """Send OTP via SMS using Twilio."""
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=f"Your TailoRent verification code is: {otp_code}. This code expires in 10 minutes.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number,
        )

        logger.info(f"OTP SMS sent to {phone_number}")
        return f"OTP SMS sent to {phone_number}"

    except Exception as e:
        logger.error(f"Failed to send OTP SMS: {str(e)}")
        raise


@shared_task
def send_welcome_email(user_id):
    """Send welcome email to new user."""
    try:
        from .models import User

        user = User.objects.get(id=user_id)

        subject = "Welcome to TailoRent!"
        message = f"""
        Hi {user.first_name or 'there'},
        
        Welcome to TailoRent! Your account has been successfully created.
        
        You can now:
        - Browse and book services from talented tailors and fashion designers
        - List your own services if you're a professional
        - Connect with the fashion community
        
        Get started by visiting our platform and exploring the available services.
        
        Best regards,
        The TailoRent Team
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        logger.info(f"Welcome email sent to {user.email}")
        return f"Welcome email sent to {user.email}"

    except Exception as e:
        logger.error(f"Failed to send welcome email: {str(e)}")
        raise


@shared_task
def send_booking_confirmation_email(booking_id):
    """Send booking confirmation email."""
    try:
        from apps.bookings.models import Booking

        booking = Booking.objects.get(id=booking_id)

        subject = "Booking Confirmation - TailoRent"
        message = f"""
        Hi {booking.customer.first_name or 'there'},
        
        Your booking has been confirmed!
        
        Service: {booking.service_type}
        Professional: {booking.professional.get_full_name()}
        Date: {booking.date}
        Location: {booking.location or 'To be discussed'}
        
        You can track your booking status in your dashboard.
        
        Best regards,
        The TailoRent Team
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.customer.email],
            fail_silently=False,
        )

        logger.info(f"Booking confirmation email sent to {booking.customer.email}")
        return f"Booking confirmation email sent to {booking.customer.email}"

    except Exception as e:
        logger.error(f"Failed to send booking confirmation email: {str(e)}")
        raise
