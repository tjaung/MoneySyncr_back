import os
import django

# Ensure the correct settings module is loaded
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "budgetTracker.settings")

# Initialize Django
django.setup()

# Now you can safely use Django components like send_mail
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test email.',
    'moneysyncr@gmail.com',
    ['jaungt@gmail.com'],
    fail_silently=False,
)