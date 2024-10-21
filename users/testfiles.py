import os

from django.conf import settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "budgetTracker.settings")

import django
django.setup()

from django.core.management import call_command
print(settings)