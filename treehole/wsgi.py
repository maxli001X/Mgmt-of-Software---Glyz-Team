"""
WSGI config for treehole project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from django.db import OperationalError, ProgrammingError


def _run_startup_migrations() -> None:
    """
    Ensure database schema is up to date when the application boots.

    Render's free tier cannot run post-deploy hooks, so we attempt to apply
    migrations programmatically. Multiple workers may invoke this concurrently,
    but Django's migrate command is idempotent, so the extra calls are harmless.
    """

    try:
        call_command('migrate', interactive=False, run_syncdb=True)
    except (OperationalError, ProgrammingError):
        # Database is unavailable or migrations cannot run yet; fail silently so the
        # app can still start. Subsequent requests will retry if the command is rerun.
        pass


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'treehole.settings')

_run_startup_migrations()

application = get_wsgi_application()
