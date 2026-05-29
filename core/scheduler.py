from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from core.cleanup import cleanup_expired_registration_sessions
from django.conf import settings

scheduler = BackgroundScheduler()

CLEANUP_JOBS = [
    {
        'func': cleanup_expired_registration_sessions,
        'id': 'cleanup_registration_sessions',
        'name':"Clean up expired registration sessions"
    }
]

def start_scheduler():
    if scheduler.running:
        return

    for job in CLEANUP_JOBS:
        scheduler.add_job(
            func=job['func'],
            trigger=IntervalTrigger(minutes=settings.SESSION_CLEANUP_INTERVAL_MINUTES),
            id=job['id'],
            name=job['name'],
            replace_existing=True
        )

    scheduler.start()

    print(
        f"[Scheduler] Started - cleanup runs every "
        f"30 minutes"
    )

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print(f"[Scheduler] Shutdown")
