import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ckl_challenge.settings")

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = DjangoWhiteNoise(get_wsgi_application())