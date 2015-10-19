#!/bin/sh
/home/job/ssbc/env/bin/gunicorn -k gevent -b :8000 ssbc.wsgi -k gevent --env DJANGO_SETTINGS_MODULE=ssbc.debug --pid /tmp/debug_ssbc -w 1

