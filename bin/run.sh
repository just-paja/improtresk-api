#!/usr/bin/env bash

app="improtresk-api"

DIR_ROOT="$(dirname "$(readlink -f "$0")")"

cd $DIR_ROOT

source ../../bin/activate

python ../manage.py migrate
python ../manage.py collectstatic --no-input
python ../manage.py check --deploy
python ../manage.py runserver 0.0.0.0:${DJANGO_PORT}
