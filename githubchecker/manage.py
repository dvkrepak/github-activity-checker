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

    # Put here your token
    TOKEN = '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'
    ACTIVE_PARSER = True  # Change if you (don't) want to activate parser

    # Parser
    # Change this if you want to parse faster/slower
    # However, do not forget about GitHub requests' limitation
    AMOUNT_OF_REQUEST_PER_MINUT = 5

    while ACTIVE_PARSER:
        GHParser.parse(TOKEN)
        time.sleep(60 // AMOUNT_OF_REQUEST_PER_MINUT)
    # End


if __name__ == '__main__':
    main()
