from celery import Celery

app = Celery('celery_module',
             broker='amqp://guest@rabbit//',
             backend='rpc://',
             include=['celery_module.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'celery_module.tasks.query_tweets',
        'schedule': 30.0,
        'args': ("Summer lang:en",)
    },
}
app.conf.timezone = 'UTC'


if __name__ == '__main__':
    app.start()