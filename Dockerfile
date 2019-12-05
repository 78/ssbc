FROM node:10.17.0-jessie

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y libodbc1 && npm install -g pm2 \
    && mkdir /data && cd /data \
    && wget -q --no-check-certificate https://repo.mongodb.org/apt/debian/dists/jessie/mongodb-org/3.2/main/binary-amd64/mongodb-org-server_3.2.10_amd64.deb \
    && wget -q --no-check-certificate https://sphinxsearch.com/files/sphinxsearch_2.3.2-beta-1~jessie_amd64.deb \
    && dpkg -i *.deb && rm -f *.deb \
    && sed -i 's/127.0.0.1/0.0.0.0/' /etc/mongod.conf

ADD . /ssbc
WORKDIR /ssbc

RUN chmod a+x /ssbc/entrypoint.sh \
    && cd spider && npm install && cd .. \
    && cd web && npm install && npm run build && cd .. \
    && mkdir -p /data/bt/index/db /data/bt/index/binlog
    

VOLUME ["/var/lib/mongodb"]
EXPOSE 27017 3001 6881/udp 

ENTRYPOINT ["/ssbc/entrypoint.sh"]

