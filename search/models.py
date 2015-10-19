#coding: utf8
import json
import re
import traceback
import binascii
import time

from django.db import models
import MySQLdb as mdb
import MySQLdb.cursors


search_conn = mdb.connect('127.0.0.1', 'root', '', '', port=9306, charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
search_conn.ping(True)
re_punctuations = re.compile(
    ur"。|，|,|！|…|!|《|》|<|>|\"|'|:|：|？|\?|、|\||“|”|‘|’|；|\\|—|_|=|（|）|·|\(|\)|　|\.|【|】|『|』|@|&|%|\^|\*|\+|\||<|>|~|`|\[|\]")


def escape_string(string):
    return re.sub(r"(['`=\(\)|\-!@~\"&/\\\^\$])", r"\\\1", string)

def split_words(string):
    string = re_punctuations.sub(u' ', string).replace(u'-', u' ')
    words = []
    for w in string.split():
        try:
            words.append(w.encode('ascii').decode('ascii'))
        except:
            for c in w:
                words.append(c)
    return u'|'.join(words).strip(u'|')


class HashManager(models.Manager):
    def search(self, keyword, start=0, count=10, category=None, sort=None):
        search_cursor = search_conn.cursor()
        sql = '''SELECT id FROM rt_main'''
        conds = []
        values = []
        if keyword:
            conds.append('MATCH(%s)')
            values.append(escape_string(keyword))
        if category:
            conds.append('category=%s')
            values.append(binascii.crc32(category)&0xFFFFFFFFL)
        if conds:
            sql += ' WHERE ' + ' AND '.join(conds)
        if sort == 'create_time':
            sql += ' ORDER BY create_time DESC '
        elif sort == 'length':
            sql += ' ORDER BY length DESC '
        sql += '''
            LIMIT %s,%s
            OPTION max_matches=1000, max_query_time=200
        '''
        search_cursor.execute(sql, values + [start, count])
        items = list(search_cursor.fetchall())
        search_cursor.execute('SHOW META')
        meta = {}
        for d in search_cursor.fetchall():
            meta[d['Variable_name']] = d['Value']
        sql = '''SELECT category, COUNT(*) AS num FROM rt_main '''
        if conds:
            sql += ' WHERE ' + ' AND '.join(conds)
        sql += ''' GROUP BY category OPTION max_query_time=200'''
        search_cursor.execute(sql, values)
        cats = list(search_cursor.fetchall())
        
        res = {
            'result': {
                'items': items,
                'meta': meta,
            },
            'cats': {
                'items': cats,
            },
        }
        search_cursor.close()
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
                    try:
                        x['files'] = json.loads(y['file_list'])
                    except ValueError:
                        pass
        items = Extra.objects.filter(hash_id__in=ids).values()
        for x in res:
            for y in items:
                if x['id'] == y['hash_id']:
                    x['extra'] = y
        return res

    def list_related(self, hash_id, name, count=10):
        string = split_words(name)
        if not string:
            return []
        search_cursor = search_conn.cursor()
        try:
            sql = '''SELECT id FROM rt_main WHERE MATCH(%s) AND id<>%s LIMIT 0,%s OPTION max_matches=1000, max_query_time=50'''
            search_cursor.execute(sql, (string, hash_id, count))
            ids = [x['id'] for x in search_cursor.fetchall()]
            items = Hash.objects.only('name', 'length', 'create_time', 'id').filter(id__in=ids).values()
        except:
            traceback.print_exc()
            items = []
        search_cursor.close()
        return items


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

    def is_blacklisted(self):
        try:
            return self.extra.status == 'disabled'
        except:
            return False


class Extra(models.Model):
    STATUS = (
        ('', 'Normal'),
        ('reviewing', 'Reviewing'),
        ('disabled', 'Disabled'),
        ('deleted', 'Deleted'),
    )
    hash = models.OneToOneField(Hash)
    status = models.CharField('Status', choices=STATUS, max_length=20)
    update_time = models.DateTimeField('更新时间', auto_now=True)


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


class ContactEmail(models.Model):
    mail_from = models.CharField('Mail From', max_length=100)
    subject = models.CharField('Subject', max_length=200)
    text = models.TextField('Text')
    receive_time = models.DateTimeField(auto_now_add=True)
    is_complaint = models.BooleanField(default=False)



