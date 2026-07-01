from celery import Celery
from app.core.config import settings

#AMQP stands for: Advanced Message Queuing Protocol
# gues:guest are username and password
#Store Celery task results in Redis.
#redis  -> Docker service name
#6379   -> Redis port
#0      -> Redis database number
celery_app = Celery("auth_service", broker=f"amqp://guest:guest@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}//",
                    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0")
celery_app.conf.imports = ("app.tasks.email_tasks",)
