if [[ $# -gt 0 ]]; then
    echo "run \"$@\""
    sh -c "$@"
else
    echo "Waiting for master database..."
    while ! nc -z ${POSTGRES_DB_HOST_MASTER} ${POSTGRES_DB_HOST_MASTER_PORT:-5432}; do sleep 1; done
    echo "Connected to master database."
    echo "Waiting for read database..."
    while ! nc -z ${POSTGRES_DB_HOST_READ} ${POSTGRES_DB_HOST_READ_PORT:-5432}; do sleep 1; done
    echo "Connected to read database."

    echo "runserver"
    python manage.py migrate --noinput

    python manage.py collectstatic --noinput
#    python manage.py create_groups

fi
# start django server
gunicorn --config gunicorn_config.py bitrate.wsgi:application
