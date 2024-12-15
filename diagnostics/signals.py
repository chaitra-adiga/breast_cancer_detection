# filepath: /c:/Users/chait/Desktop/breast_cancer_detection/diagnostics/signals.py
import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Diagnostic

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Diagnostic)
def send_patient_added_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to BCD System'
        html_message = render_to_string('diagnostics/email_template.html', {
            'user_name': instance.user_name,
            'user_phn': instance.user_phn,
            'login_url': 'http://127.0.0.1:8000/user-login/'  # Update with your site's URL
        })
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = instance.email_id

        try:
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        except Exception as e:
            logger.error(f"Error sending email: {e}")