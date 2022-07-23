#!/bin/sh
echo "-----Collectstatic-----"
python manage.py collectstatic --noinput

echo "-----Make migrations-----"
python manage.py makemigrations --noinput

echo "-----Migrate-----"
python manage.py migrate --noinput

echo "-----Run server-----"
gunicorn shipment.wsgi:application --bind 0.0.0.0:8000 --timeout 300000
