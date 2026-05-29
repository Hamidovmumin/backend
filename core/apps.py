from django.apps import AppConfig
import atexit

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from core.scheduler import start_scheduler,shutdown_scheduler
        start_scheduler()
        atexit.register(shutdown_scheduler)