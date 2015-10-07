#!/bin/sh
/home/job/ssbc/env/bin/gunicorn -k gevent -b :8002 ssbc.wsgi -k gevent --env DJANGO_SETTINGS_MODULE=ssbc.deployment --pid /tmp/ssbc.pid -w 6

