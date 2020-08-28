web: gunicorn force_account_generator.wsgi --log-file -
worker: celery worker --app=force_account_generator -l info
web-dev: python manage.py runserver
worker-dev: celery worker --app=force_account_generator --pool=solo -l info