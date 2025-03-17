#!/bin/sh 

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
      echo "Connection is not successfull, trying again..."
    done

    echo "PostgreSQL started"
fi

python manage.py migrate --settings=config.settings.production
python manage.py collectstatic --settings=config.settings.production --no-input
exec "$@"