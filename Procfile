web: gunicorn --pythonpath force_account_generator force_account_generator.wsgi --log-file -
worker: celery worker --app=force_account_generator/force_account_generator -l info
web-dev: python force_account_generator/manage.py runserver
worker-dev: celery worker --pythonpath force_account_generator --app=force_account_generator --pool=solo -l info