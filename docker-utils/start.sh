#!/bin/bash
echo "Starting Gunicorn."

cd $PROJECT_ROOT

export PYTHONPATH="${PROJECT_ROOT}/example/:${PYTHONPATH}"

if [ ! -f $PROJECT_ROOT/.build ]; then
  echo "Collecting and compiling statics."
  python example/manage.py collectstatic --noinput
  date > $PROJECT_ROOT/.build
fi

exec gunicorn example.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
