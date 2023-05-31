#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'githubchecker.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    from checker.utils import GHParser
    import time
    # TOKEN = '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'
    # while True:
    #     GHParser.parse(TOKEN)
    #     time.sleep(1)



if __name__ == '__main__':
    main()
