from celery import Celery
from common.config import config

config = {
    "broker_url": config["redis_urls"]["tasks"],
    "result_backend": config["redis_urls"]["tasks_results"],
    "result_expires": 15,
    "task_track_started": True,
    "worker_state_db": "workerstate",
}

app = Celery(
    "server",
    config_source=config,
)
