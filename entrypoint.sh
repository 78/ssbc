#!/bin/bash

/usr/bin/mongod --quiet --config /etc/mongod.conf --fork

sleep 6

cd /ssbc/spider && pm2 start ecosystem.config.js && cd ..

cd web && pm2 start ecosystem.config.js && cd ..

trap 'kill $(pgrep searchd) 2>/dev/null; pm2 kill; kill $(pgrep mongod); exit 0' SIGINT SIGTERM

sleep 3 &
wait

cd spider
if [ ! -e /data/.inited ]; then
	indexer -c sphinx.conf hash &
	wait
	echo 1 >/data/.inited
fi
searchd -c sphinx.conf && cd ..

sleep infinity &
wait

