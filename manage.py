#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ckl_challenge.settings")

    if 'worker' in sys.argv:
        from rss.worker import run
        import django

        django.setup()

        run()
    else:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
