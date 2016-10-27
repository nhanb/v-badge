from flask import Flask
from .task_queue import make_celery


app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='amqp://vbadge_user:vbadge_user@localhost:5672//',
    CELERY_RESULT_BACKEND='db+sqlite:///results.sqlite'
)
celery_app = make_celery(app)


import vbadge.views
