#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import environ

env = environ.Env()
env.read_env()


def main():
    is_production = env('PRODUCTION', cast=bool)
    print("is_production", is_production)
    if is_production:
        print("...production...")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_api.settings.production')
    else:
        print("...development...")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_api.settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
