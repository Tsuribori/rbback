#!/bin/sh

if [[ $DEVELOPMENT ]]; then
  settings_module=rbback.dev_settings
else
  settings_module=rbback.prod_settings
fi

# Create compressed tarball of source to static folder to be served.
tar --exclude-from=.gitignore --exclude .git -czvf rbback/static/rbback.tar.gz .

cd rbback
until python manage.py migrate --no-input --settings=$settings_module; do
  sleep 2
  echo "Database not up yet, waiting...";
done

python manage.py collectstatic --no-input

if [[ $DEVELOPMENT ]]; then
  python manage.py runserver 0.0.0.0:8000 --settings=$settings_module
else
  gunicorn --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=$settings_module --error-logfile - rbback.wsgi:application
fi
