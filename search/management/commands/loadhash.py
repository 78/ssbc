#coding: utf8
from django.core.management.base import BaseCommand
from django import db as ddb
from search.models import Hash
import pymongo

db = pymongo.MongoClient().dht

class Command(BaseCommand):
    def handle(self, *args, **options):
        Hash.objects.all().delete()
        print 'inputing ...'
        total = db.basic.count()
        ii = 0
        ready = []
        for x in db.basic.find():
            ii += 1
            if ii % 10000 == 0:
                print ii * 100 / total, '%', total - ii
                Hash.objects.bulk_create(ready)
                ready = []
                ddb.reset_queries()

            h = Hash(info_hash = x['info_hash'])
            h.classified = x.get('classified', False)
            h.tagged = x.get('tagged', False)

            h.name = unicode(x.get('name',''))[:255]
            h.category = x.get('category','')[:20]
            h.extension = x.get('extension', '')[:20]
            h.data_hash = x.get('data_hash', '')
            h.comment = x.get('comment','')[:255]
            h.creator = x.get('creator','')[:20]

            h.length = x.get('length', 0)
            h.requests = x.get('requests', 0)
            h.source_ip = x.get('source_ip')
            h.create_time = x.get('create_time')
            h.last_seen = x.get('last_seen', h.create_time)
            ready.append(h)

        if ready:
            Hash.objects.bulk_create(ready)
