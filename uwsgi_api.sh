#!/bin/sh
uwsgi --socket /tmp/ssbc_api.sock --http :8001 --chmod-socket=666  -w ssbc.wsgi --processes 2  --threads 10 --thunder-lock --stats 127.0.0.1:9191 -R 5000 --disable-logging  -M
