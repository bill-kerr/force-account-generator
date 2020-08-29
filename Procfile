web: gunicorn --pythonpath force_account_generator force_account_generator.wsgi --log-file -
worker: cd force_account_generator && celery worker --app=force_account_generator -l info
web-dev: python force_account_generator/manage.py runserver
worker-dev: cd force_account_generator && celery worker --app=force_account_generator --pool=solo -l info