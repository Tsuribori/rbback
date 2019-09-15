#!/bin/sh

cd rbback
until python manage.py migrate; do
  sleep 2
  echo "Database not up yet, waiting...";
done

python manage.py collectstatic --no-input

gunicorn --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=rbback.prod_settings --access-logfile - --error-logfile - rbback.wsgi:application
