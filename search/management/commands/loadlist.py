#coding: utf8
from django.core.management.base import BaseCommand
from django import db as ddb
from search.models import FileList
import pymongo
import json
import binascii

db = pymongo.MongoClient().dht

class Command(BaseCommand):
    def handle(self, *args, **options):
        #FileList.objects.all().delete()
        print 'inputing ...'
        total = db.filelist.count()
        ii = 0
        ready = []
        for x in db.filelist.find():
            ii += 1
            if ii % 200 == 0:
                try:
                    FileList.objects.bulk_create(ready)
                except:
                    for r in ready:
                        try:
                            r.save()
                        except:
                            import traceback
                            traceback.print_exc()
                ready = []
            if ii % 10000 == 0:
                print ii * 100 / total, '%', total - ii
                ddb.reset_queries()

            h = FileList()
            h.info_hash = binascii.hexlify(x['_id'])
            h.file_list = json.dumps(x['files'])
            ready.append(h)

        if ready:
            FileList.objects.bulk_create(ready)

