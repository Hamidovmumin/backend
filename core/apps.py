import os
import sys
import atexit
from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # runserver autoreload guard (lokal, həm Windows həm Linux)
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') != 'true':
            return

        # production (gunicorn, çox worker) guard — yalnız Unix-də
        if 'runserver' not in sys.argv:
            try:
                import fcntl
                lock_file = open('/tmp/scheduler.lock', 'wb')
                fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except (IOError, OSError, ImportError):
                return

        from core.scheduler import start_scheduler, shutdown_scheduler
        start_scheduler()
        atexit.register(shutdown_scheduler)