#!/usr/bin/env python2.6
#coding: utf8
"""
磁力搜索meta信息入库程序
从队列里读取hash，如果数据库里不存在，就使用libtorrent获取meta信息，保存到数据库中。
xiaoxia@xiaoxia.org
2013.5 created
2015.5 updated
"""


import cPickle
import hashlib
import time
import traceback
import datetime
import sys
import bencode
import cStringIO
import gzip
import urllib2
import binascii
import socket
import threading
import Queue
import xmlrpclib
import metautils
import libtorrent as lt
import random
import json
import threading
import MySQLdb as mdb

threading.stack_size(128000)
socket.setdefaulttimeout(60)
MAX_READ = 20
DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASS = ''
q = Queue.Queue(MAX_READ)
downloading = set()


class DHTReporter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ses = lt.session()
        self.init_libtorrent()
        self.dbconn = mdb.connect(DB_HOST, DB_USER, DB_PASS, 'ssbc', charset='utf8')
        self.dbcurr = self.dbconn.cursor()
        self.dbcurr.execute('SET NAMES utf8')

    def init_libtorrent(self):
        ses = self.ses
        r = random.randrange(10000, 50000)
        ses.listen_on(r, r+10)
        ses.add_dht_router('router.bittorrent.com',6881)
        ses.add_dht_router('router.utorrent.com',6881)
        ses.add_dht_router('dht.transmission.com',6881)
        ses.add_dht_router('70.39.87.34',6881)
        ses.start_dht()

    def fetch_torrent(self, ih):
        if ih in downloading:
            return None
        downloading.add(ih)
        name = ih.upper()
        url = 'magnet:?xt=urn:btih:%s' % (name,)
        data = ''
        params = {
            'save_path': '/tmp/downloads/',
            'storage_mode': lt.storage_mode_t(2),
            'paused': False,
            'auto_managed': False,
            'duplicate_is_error': True}
        try:
            handle = lt.add_magnet_uri(self.ses, url, params)
        except:
            downloading.remove(ih)
            return None
        status = self.ses.status()
        #print 'downloading metadata:', url
        handle.set_sequential_download(1)
        down_time = time.time()
        for i in xrange(0, 60):
            if handle.has_metadata():
                info = handle.get_torrent_info()
                print '\n', time.ctime(), (time.time()-down_time), 's, got', url, info.name()
                #print 'status', 'p', status.num_peers, 'g', status.dht_global_nodes, 'ts', status.dht_torrents, 'u', status.total_upload, 'd', status.total_download
                meta = info.metadata()
                self.ses.remove_torrent(handle)
                downloading.remove(ih)
                return meta
            time.sleep(1)
        downloading.remove(ih)
        self.ses.remove_torrent(handle)
        return None

    def decode(self, s):
        if type(s) is list:
            print 'list', s
            s = ';'.join(s)
        u = s
        for x in (self.encoding, 'utf8', 'gbk', 'big5'):
            try:
                u = s.decode(x)
                return u
            except:
                pass
        return s.decode(self.encoding, 'ignore')

    def decode_utf8(self, d, i):
        if i+'.utf-8' in d:
            return d[i+'.utf-8'].decode('utf8')
        return self.decode(d[i])

    def parse_meta(self, meta):
        info = {}
        info['create_time'] = meta.creation_time()
        info['creator'] = meta.creator()
        info['comment'] = meta.comment()
        info['name'] = meta.name()
        info['files'] = []

                
    def parse_torrent(self, data):
        info = {}
        self.encoding = 'utf8'
        torrent = bencode.bdecode(data)
        try:
            info['create_time'] = datetime.datetime.fromtimestamp(float(torrent['creation date']))
        except:
            info['create_time'] = datetime.datetime.utcnow()

        if torrent.get('encoding'):
            self.encoding = torrent['encoding']
        if torrent.get('announce'):
            info['announce'] = self.decode_utf8(torrent, 'announce')
        if torrent.get('comment'):
            info['comment'] = self.decode_utf8(torrent, 'comment')
        if torrent.get('publisher-url'):
            self.encoding = self.decode_utf8(torrent, 'publisher-url')
        if torrent.get('publisher'):
            info['publisher'] = self.decode_utf8(torrent, 'publisher')
        if torrent.get('created by'):
            info['creator'] = self.decode_utf8(torrent, 'created by')

        if 'info' in torrent:
            detail = torrent['info'] 
        else:
            detail = torrent
        info['name'] = self.decode_utf8(detail, 'name')
        if 'files' in detail:
            info['files'] = []
            for x in detail['files']:
                if 'path.utf-8' in x:
                    v = {'path': self.decode('/'.join(x['path.utf-8'])), 'length': x['length']}
                else:
                    v = {'path': self.decode('/'.join(x['path'])), 'length': x['length']}
                if 'filehash' in x:
                    v['filehash'] = binascii.hexlify(x['filehash'])
                info['files'].append(v)
            info['length'] = sum([x['length'] for x in info['files']])
        else:
            info['length'] = detail['length']
        info['data_hash'] = hashlib.md5(detail['pieces']).hexdigest()
        if 'profiles' in detail:
            info['profiles'] = detail['profiles']
        return info

    def run(self):
        self.name = threading.currentThread().getName()
        print self.name, 'started'
        n_reqs = n_valid = n_new = 0
        while True:
            x = q.get()
            n_reqs += 1

            utcnow = datetime.datetime.utcnow()
            date = (utcnow + datetime.timedelta(hours=8))
            date = datetime.datetime(date.year, date.month, date.day)
            while True:
                # Check if we have this info_hash
                self.dbcurr.execute('SELECT id FROM search_hash WHERE info_hash=%s', (x['info_hash'],))
                y = self.dbcurr.fetchone()
                if not y:
                    try:
                        data = self.fetch_torrent(x['info_hash'])
                    except:
                        traceback.print_exc()
                        break
                    if not data:
                        sys.stdout.write('!')
                        #print self.name, 'Missing torrent file', x['info_hash'], 'from', x['ip']
                        break
                    try:
                        info = self.parse_torrent(data)
                    except:
                        traceback.print_exc()
                        break
                    info['info_hash'] = x['info_hash']
                    # need to build tags
                    info['tagged'] = False
                    info['classified'] = False
                    info['requests'] = 1
                    info['last_seen'] = utcnow
                    info['source_ip'] = x['ip']

                    if info.get('files'):
                        files = [z for z in info['files'] if not z['path'].startswith('_')]
                        if not files:
                            files = info['files']
                    else:
                        files = [{'path': info['name'], 'length': info['length']}]
                    files.sort(key=lambda z:z['length'], reverse=True)
                    bigfname = files[0]['path']
                    info['extension'] = metautils.get_extension(bigfname).lower()
                    info['category'] = metautils.get_category(info['extension'])

                    if 'files' in info:
                        self.dbcurr.execute('INSERT INTO search_filelist VALUES(%s, %s)', (info['info_hash'], json.dumps(info['files'])))
                        del info['files']

                    try:
                        #db.basic.save(info, w=1)
                        ret = self.dbcurr.execute('INSERT INTO search_hash(info_hash,category,data_hash,name,extension,classified,source_ip,tagged,' + 
                            'length,create_time,last_seen,requests,comment,creator) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            (info['info_hash'], info['category'], info['data_hash'], info['name'], info['extension'], info['classified'],
                            info['source_ip'], info['tagged'], info['length'], info['create_time'], info['last_seen'], info['requests'],
                            info.get('comment',''), info.get('creator','')))
                    except:
                        print 'save error', self.name, info
                        traceback.print_exc()
                        break
                    n_new += 1
                n_valid += 1

                # Check if we have log this request
                #_id_data = '%s-%s-%s' % (x['info_hash'], x['ip'], x['port'])
                #tmpid = binascii.crc32(_id_data) & 0xffffffff
                #if db_log.requests_user.find_one({'_id': tmpid}):
                #    sys.stdout.write('S')
                #    sys.stdout.flush()
                #    break
                #db_log.requests_user.save({'_id': tmpid, 
                #    'time': utcnow})
                
                # 更新最近发现时间，请求数
                if y:
                    self.dbcurr.execute('UPDATE search_hash SET last_seen=%s, requests=requests+1 WHERE info_hash=%s', (utcnow, x['info_hash']))

                # 更新日请求量统计
                #colname = 'requests_d_' + date.strftime('%y%m%d')
                #db_log[colname].update(
                #    {'_id': bid}, 
                #    {'$inc': {'requests': 1}}
                #    , upsert=True)
                sys.stdout.write('#')
                sys.stdout.flush()
                self.dbconn.commit()
                break

            if n_reqs >= MAX_READ:
                self.dbcurr.execute('INSERT INTO search_statusreport(date,new_hashes,total_requests, valid_requests)  VALUES(%s,%s,%s,%s) ON DUPLICATE KEY UPDATE ' +
                    'total_requests=total_requests+%s, valid_requests=valid_requests+%s, new_hashes=new_hashes+%s',
                    (date, n_new, n_reqs, n_valid, n_reqs, n_valid, n_new))
                    
                n_reqs = n_valid = n_new = 0

def load_queue_from_rpc():
    rpc = xmlrpclib.ServerProxy('http://127.0.0.1:8803')
    while True:
        try:
            t = rpc.get_req()
            q.put(t)
        except KeyboardInterrupt:
            break
        except:
            print sys.exc_info()[1]
            time.sleep(1)


if __name__ == '__main__':
    for x in xrange(MAX_READ):
        reporter = DHTReporter()
        reporter.start()
    load_queue_from_rpc()

