#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path)

print("DEBUG ENV:", os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
print("EXISTS:", os.path.exists(os.getenv('GOOGLE_APPLICATION_CREDENTIALS')))

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')
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