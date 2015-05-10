#!/bin/sh
uwsgi --socket /tmp/ssbc_www1.sock --http :8002 --chmod-socket=666  -w ssbc.wsgi --processes 2  --threads 20 --thunder-lock --stats 127.0.0.1:9192 -R 5000 --disable-logging  -M
