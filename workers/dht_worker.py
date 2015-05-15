#!/usr/bin/env python
#coding: utf8
"""
磁力搜索爬虫代码
爬虫获取的hash地址会放进队列，由负责下载资源信息的meta_worker处理和入库。
xiaoxia@xiaoxia.org
2013.5 created
2015.5 updated
"""

import bencode
import sys
import xmlrpclib
import traceback
import urllib2
import struct
import threading
import random
import socket
import cPickle
import time
import hashlib
import binascii
import datetime
import Queue
from SimpleXMLRPCServer import SimpleXMLRPCServer

DHT_PORT = 6881
DHT_IP = socket.gethostbyname(socket.gethostname())

req_queue = Queue.Queue(1000)

class DHT(threading.Thread):
    def __init__(self):
        global DHT_PORT
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.mutex = threading.RLock()
        self.next_sequence = 0
        for i in xrange(10):
            try:
                self.udp_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                self.udp_fd.bind((DHT_IP, DHT_PORT))
                break
            except:
                DHT_PORT += 1
        print 'Bind socket at %s:%s' % (DHT_IP, DHT_PORT)
        self.node_id = self.get_random_id()
        self.version = 'XTxx'
        self.new_nodes = Queue.Queue()
        self.visited_nodes = []
        self.visited_count = 0
        self.logs = set()
        self.speed_start = time.time()
        self.speed_counter = 0
        self.speed = 0

    def get_random_id(self):
        s = []
        for x in xrange(20):
            s.append(random.randrange(0,256))
        return ''.join(map(chr, s))

    def run(self):
        while True:
            data, addr = self.udp_fd.recvfrom(65536)
            try:
                msg = bencode.bdecode(data)
                try:
                    self.recv_message(msg, addr)
                except:
                    print '[ERROR]', msg
            except:
                print '[ERROR]', repr(data)
            if self.new_nodes.qsize() < 10000:
                continue
            #time.sleep(.1)

    def lock(self):
        self.mutex.acquire()
    def unlock(self):
        self.mutex.release()

    def new_sequence(self):
        seq = '%8d' % (self.next_sequence % 65536*65535)
        self.next_sequence += 1
        return seq

    def send_message(self, addr, msg):
        #if msg['y'] == 'r':
        #print '[S]', msg, 'to', addr
        if not addr[1]:
            return
        data = bencode.bencode(msg)
        try:
            self.udp_fd.sendto(data, addr)
        except:
            print '[ERROR] sending', msg, 'to', addr

    def ping(self, addr):
        m = {
            'v': self.version,
            't': self.new_sequence(),
            'y': 'q',
            'q': 'ping',
            'a': {
                'id': self.node_id,
            }
        }
        self.send_message(addr, m)

    def find_node(self, addr, target_id):
        m = {
            'v': self.version,
            't': self.new_sequence(),
            'y': 'q',
            'q': 'find_node',
            'a': {
                'id': self.node_id,
                'target': target_id,
            }
        }
        self.send_message(addr, m)

    def get_peers(self, addr, info_hash):
        m = {
            'v': self.version,
            't': self.new_sequence(),
            'y': 'q',
            'q': 'get_peers',
            'a': {
                'id': self.node_id,
                'info_hash': info_hash,
            }
        }
        self.send_message(addr, m)

    def distance(self, a, b):
        dist = sum([bin(ord(x) ^ ord(y)).count('1') for x,y in zip(a,b)])
        return dist

    def get_neighbor_nodes(self, target):
        strings = []
        nodes = []
        self.lock()
        temp_nodes = self.visited_nodes[:50]
        self.unlock()
        for x in temp_nodes:
            dist = self.distance(target, x['info_hash'])
            nodes.append((dist, x))
        nodes.sort()
        for dist, x in nodes:
            s = '%s%s%s' % (x['info_hash'], socket.inet_aton(x['addr'][0]), struct.pack('!H', x['addr'][1]))
            strings.append(s)
            if len(strings) >= 8:
                break
        return ''.join(strings)

    def get_self_nodes(self, target):
        nodes = []
        nodes.append('%s%s%s' % (self.node_id, socket.inet_aton(DHT_IP), struct.pack('!H', DHT_PORT)))
        return ''.join(nodes)

    def get_token(self, addr):
        return socket.inet_aton(addr[0])

    def recv_message(self, msg, addr):
        if msg['y'] == 'q':
            a = msg['a']
            if msg['q'] == 'ping':
                m = {
                    't': msg['t'],
                    'y': 'r',
                    'r': {'id': self.get_random_id()},
                }
                self.send_message(addr, m)
            elif msg['q'] == 'find_node':
                m = {
                    't': msg['t'],
                    'y': 'r',
                    'r': {'id': self.node_id,
                        'nodes': self.get_self_nodes(a['target'])
                    }
                }
                self.send_message(addr, m)
            elif msg['q'] == 'get_peers':
                self.log_info_hash(addr, a['info_hash'], msg.get('v',''))
                m = {
                    't': msg['t'],
                    'y': 'r',
                    'r': {'id': self.node_id,
                        'token': self.get_token(addr),
                        'nodes': self.get_neighbor_nodes(a['info_hash'])
                    }
                }
                self.send_message(addr, m)
            elif msg['q'] == 'announce_peer':
                a = '%s:%s' % (addr[0], a['port'])
                self.log_info_hash(addr, a['info_hash'], msg.get('v',''))
            else:
                print '[R]', msg, 'from', addr
                raise Exception('not handled.')

        elif msg['y'] == 'r':
            r = msg['r']
            if 'nodes' in r:
                self.parse_nodes(r['nodes'])
            if 'values' in r:
                if type(r['values']) is str:
                    for start in xrange(0, len(r['values']), 6):
                        ip, port = r['values'][start:start+4], r['values'][start+4:start+6]
                        print ip, port, r['values']
                        ip = socket.inet_ntoa(struct.unpack('!I', ip)[0])
                        port = socket.ntohs(port)
                        key = '%s:%s' % ip, port
                        #print 'peer', key

        elif msg['y'] == 'e':
            #print '[R]', msg, 'from', addr
            pass

    def parse_nodes(self, nodes):
        for i in xrange(0, len(nodes), 26):
            info_hash = nodes[i:i+20]
            ip = socket.inet_ntoa(nodes[i+20:i+24])
            port = struct.unpack('!H', nodes[i+24:i+26])[0]
            self.add_node((ip, port), info_hash)

    def add_node(self, addr, info_hash):
        if addr[0] == DHT_IP:
            return
        timenow = datetime.datetime.now()
        # 保持未请求得节点队列不太长
        if self.new_nodes.qsize() < 10000:
            self.new_nodes.put({
                'addr': addr,
                'info_hash': info_hash,
                'refresh_time': timenow,
            })

    def auto_find(self):
        temp = []
        while self.new_nodes.qsize() > 0:
            v = self.new_nodes.get()
            temp.append(v)
            self.visited_count += 1
            if self.visited_count % 10000 == 0:
                print '\nVISITED NODE COUNT', self.visited_count, 'NEW', self.new_nodes.qsize(), 'SPEED', self.speed
            if len(temp) > 1000:
                self.lock()
                self.visited_nodes = temp
                self.unlock()
                temp = []
            self.get_peers(v['addr'], self.get_random_id())

    def log_info_hash(self, addr, info_hash, version):
        #print 'INFO_HASH', binascii.hexlify(info_hash), 'from', addr
        req = {
            'info_hash': binascii.hexlify(info_hash),
            'ip': addr[0],
            'port': addr[1],
            'source': '%s:%s' % (DHT_IP, DHT_PORT),
        }
        print req
        sys.stdout.write('+')
        sys.stdout.flush()
        req_queue.put(req)

        self.speed_counter += 1
        if time.time() - self.speed_start >= 10:
            self.speed = self.speed_counter * 6
            self.speed_counter = 0
            self.speed_start = time.time()

def get_req():
    sys.stdout.write('-')
    sys.stdout.flush()
    t = req_queue.get()
    return t

def start_rpcserver():
    rpcsrv = SimpleXMLRPCServer(("0.0.0.0", 8803), logRequests=False)
    rpcsrv.register_function(get_req, 'get_req')
    print 'XMLRPC server is running on', rpcsrv.server_address
    rpcsrv.serve_forever()

if __name__ == '__main__':
    rpcthread = threading.Thread(target=start_rpcserver)
    rpcthread.setDaemon(True)
    rpcthread.start()

    dht = DHT()
    dht.start()
    dht.find_node(('router.bittorrent.com',6881), dht.get_random_id())
    dht.find_node(('router.utorrent.com',6881), dht.get_random_id())
    dht.find_node(('dht.transmission.com',6881), dht.get_random_id())
    while True:
        dht.auto_find()
        time.sleep(.1)



