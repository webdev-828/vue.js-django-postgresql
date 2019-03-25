web: gunicorn invtask.app.wsgi
worker: celery worker -A invtask.app.celery --loglevel=info --logfile=worker.log -B
