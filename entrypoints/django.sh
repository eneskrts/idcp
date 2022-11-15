#!/bin/bash -x
echo "Django shell script is running ..."
python manage.py collectstatic --noinput --settings=idcp_project.settings.production &&
#python manage.py makemigrations --settings=idcp_project.settings.production &&
python manage.py migrate --noinput --settings=idcp_project.settings.production &&
python manage.py runserver 0.0.0.0:8000 --settings=idcp_project.settings.production &&
gunicorn idcp_project.wsgi:application --bind 0.0.0.0:8000

exec "$@"
