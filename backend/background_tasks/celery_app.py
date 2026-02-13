from celery import Celery
from core.config import settings

celery_app = Celery(
    "creator_os",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['background_tasks.tasks']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

celery_app.conf.beat_schedule = {
    'sync-instagram-data-daily': {
        'task': 'background_tasks.tasks.sync_instagram_data_all_pages',
        'schedule': 86400.0,
    },
    'generate-weekly-intelligence-summary': {
        'task': 'background_tasks.tasks.generate_weekly_intelligence_summary',
        'schedule': 604800.0,
    },
    'retrain-models-weekly': {
        'task': 'background_tasks.tasks.retrain_virality_models',
        'schedule': 604800.0,
    },
}
