#!/bin/sh
set -e

# Go to directory
cd $PROJECT_PATH

# Activate virtualenv
source .venv/bin/activate

# Static files
python manage.py collectstatic --noinput

# Change permission
chmod 775 -R $PROJECT_PATH
chown app:app -R $PROJECT_PATH

# Test
if [[ $DJANGO_SETTINGS_MODULE == 'config.settings_test' ]]; then
    echo "Run testing mode"

    # Run test
    exec gosu app python manage.py test --noinput
    exit
else
    echo "Run production mode"

    # Run migration
    gosu app python manage.py migrate

    # Run project
    exec gosu app gunicorn config.wsgi -b 0.0.0.0:8000
    exit
fi

