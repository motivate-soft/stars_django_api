#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import environ

try:
    import googleclouddebugger

    googleclouddebugger.enable(
        breakpoint_enable_canary=True
    )
except ImportError:
    pass

env = environ.Env()
env.read_env()


def main():
    debug_mode = env('DEBUG', cast=bool)
    if debug_mode:
        print("...development...")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_api.settings.development')
    else:
        print("...production...")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_api.settings.production')
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
