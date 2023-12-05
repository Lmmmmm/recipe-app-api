#!/bin/sh


set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi

# set -e

# python manage.py wait_for_db
# #collect all of the static files and put them in the configured static files directory.
# python manage.py collectstatic --noinput
# #run any migrations automatically whenever we start app. database will migrated to the correct state
# python manage.py migration
# # app.wsgi means the entry point to our project is app.wsgi(app/app/wsgi.py), beacuse we will start from app folder by docker compose
# uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi