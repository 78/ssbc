#coding: utf8
from django.core.management.base import BaseCommand
from django import db as ddb
from search.models import StatusReport
import pymongo

db = pymongo.MongoClient().dht

class Command(BaseCommand):
    def handle(self, *args, **options):
        StatusReport.objects.all().delete()
        print 'inputing ...'
        for x in db.report_total_d.find().sort('date', 1):
            r = StatusReport()
            r.date = x['date']
            r.new_hashes = x['new_hashes']
            r.total_requests = x['total_requests']
            r.valid_requests = x['valid_requests']
            r.save()


