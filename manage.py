#!/usr/bin/env python
import sys

import os


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ckl_challenge.settings")

    if 'worker' in sys.argv:
        sys.argv.remove('worker')
        import django

        django.setup()

        from rss.worker import Worker

        worker = Worker(minutes=5)
        worker.start()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
