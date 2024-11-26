#!/bin/bash

if [ ! -f "/opt/pecoret/conf/production.py" ]; then
    touch /opt/pecoret/conf/__init__.py
    cp docker/local_settings.template.py /opt/pecoret/conf/production.py
fi

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

echo "collect static files"
python manage.py collectstatic --noinput

echo "Import CWE entries"
python manage.py import_cwe_entries
# create superuser
echo "Create superuser"
python manage.py createsuperuser --noinput

# Start server
echo "Starting server"
gunicorn --bind 0.0.0.0:8000 pecoret.wsgi --daemon
nginx -g 'daemon off;'
