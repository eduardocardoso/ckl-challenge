import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ckl_challenge.settings")

import django

django.setup()

from rss.worker import Worker

worker = Worker(minutes=10)
worker.start()
worker.join()
