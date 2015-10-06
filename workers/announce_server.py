#coding: utf8
import sys
import time
import urlparse
import datetime
import xmlrpclib

from flask import Flask, request, abort
import pygeoip

from bencode import bencode

geoip = pygeoip.GeoIP('GeoIP.dat')

app = Flask(__name__)
app.debug = False
rpc = xmlrpclib.ServerProxy('http://127.0.0.1:8004')

@app.route('/announce.php')
def announce():
    '''/announce.php?info_hash=&peer_id=&ip=&port=&uploaded=&downloaded=&left=&numwant=&key=&compact=1'''
    ip = request.args['ip']
    port = request.args['port']
    address = (ip, int(port))
    binhash = urlparse.parse_qs(request.query_string)['info_hash'][0]
    country = geoip.country_code_by_addr(ip)
    if country not in ('CN','TW','JP','HK'):
        return abort(404)
    rpc.announce(binhash.encode('hex'), address)
    return bencode({'peers': '', 'interval': 86400})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005)

