#coding: utf8
import json
import binascii

from django.db import models
from sphinxit.core.helpers import BaseSearchConfig
from sphinxit.core.processor import Search
from sphinxit.core.nodes import Count


class SphinxitConfig(BaseSearchConfig):
    WITH_STATUS = False


class HashManager(models.Manager):
    def search(self, keyword, start=0, count=10, category=None, sort=None):
        search_query = Search(indexes=['rt_main'], config=SphinxitConfig)
        q = search_query.match(keyword)
        if category: q = q.filter(category__eq=binascii.crc32(category)&0xFFFFFFFFL)
        if sort == 'create_time': q = q.order_by('create_time', 'desc')
        if sort == 'length': q = q.order_by('length', 'desc')
        q = q.limit(start, count)
        q2 = search_query.match(keyword).select('category', Count()).group_by('category').named('cats')
        res = q.ask(subqueries=[q2])
        return res

    def list_with_files(self, ids):
        res = []
        if len(ids[0]) == 40:
            items = Hash.objects.filter(info_hash__in=ids).values()
        else:
            items = Hash.objects.filter(id__in=ids).values()
        res = list(items)
        items = FileList.objects.filter(info_hash__in=[x['info_hash'] for x in res]).values()
        for x in res:
            for y in items:
                if x['info_hash'] == y['info_hash']:
                    x['files'] = json.loads(y['file_list'])
        return res

class Hash(models.Model):
    objects = HashManager()

    info_hash = models.CharField(max_length=40, unique=True)
    category = models.CharField('类别', max_length=20)
    data_hash = models.CharField('内容签名', max_length=32)
    name = models.CharField('资源名称', max_length=255)
    extension = models.CharField('扩展名', max_length=20)
    classified = models.BooleanField('是否分类', default=False)
    source_ip = models.CharField('来源IP', max_length=20, null=True)
    tagged = models.BooleanField('是否索引', default=False, db_index=True)
    length = models.BigIntegerField('文件大小')
    create_time = models.DateTimeField('入库时间')
    last_seen = models.DateTimeField('上次请求时间')
    requests = models.PositiveIntegerField('请求次数')
    comment = models.CharField(max_length=255, null=True)
    creator = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return self.name


class FileList(models.Model):
    info_hash = models.CharField(max_length=40, primary_key=True)
    file_list = models.TextField('JSON格式的文件列表')

    def __unicode__(self):
        return self.info_hash


class StatusReport(models.Model):
    date = models.DateField('日期', unique=True)
    new_hashes = models.IntegerField('新增资源')
    total_requests = models.IntegerField()
    valid_requests = models.IntegerField()

    def __unicode__(self):
        return u'%s - %s' % (self.date, self.new_hashes)


class RecKeywords(models.Model):
    keyword = models.CharField('推荐关键词', max_length=20)
    order = models.PositiveIntegerField('排序', default=0)

    def __unicode__(self):
        return u'%s %s' % (self.keyword, self.order)


