from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from core.cleanup import cleanup_expired_registration_sessions
from django.conf import settings
from services.currency_service import fetch_currency_rates

scheduler = BackgroundScheduler()

CLEANUP_JOBS = [
    {
        'func': cleanup_expired_registration_sessions,
        'id': 'cleanup_registration_sessions',
        'name':"Clean up expired registration sessions",
        'minutes': settings.SESSION_CLEANUP_INTERVAL_MINUTES,
    },
    {
        'func': fetch_currency_rates,
        'id': 'fetch_currency_rates',
        'name':"Fetch currency rates",
        'minutes': getattr(settings, 'CURRENCY_FETCH_INTERVAL_MINUTES', 2),
    }
]

def start_scheduler():
    if scheduler.running:
        return

    for job in CLEANUP_JOBS:
        scheduler.add_job(
            func=job['func'],
            trigger=IntervalTrigger(minutes= job['minutes']),
            id=job['id'],
            name=job['name'],
            replace_existing=True
        )
        print(f"[Scheduler] '{job['name']}' başladıldı - hər {job['minutes']} dəqiqədən bir işləyəcək.")

    scheduler.start()

    print("[Scheduler] Bütün scheduler tapşırıqları uğurla işə salındı.")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print(f"[Scheduler] Shutdown")
