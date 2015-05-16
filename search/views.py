from django.shortcuts import render
from ssbc import settings
from django.http import JsonResponse, HttpResponse
from search.models import Hash, FileList, StatusReport
from sphinxit.core.helpers import BaseSearchConfig
from sphinxit.core.processor import Search
from sphinxit.core.nodes import Count
import binascii
import json
import memcache

class SphinxitConfig(BaseSearchConfig):
    WITH_STATUS = False
mc = memcache.Client(['127.0.0.1:11211'],debug=0)

# Create your views here.
def json_search(request):
    search_query = Search(indexes=['rt_main'], config=SphinxitConfig)
    keyword = request.GET['keyword']
    start = request.GET.get('start', 0)
    count = request.GET.get('count', 10)
    sort = request.GET.get('sort', '')
    category = request.GET.get('category', '')
    if request.GET.get('base64') == '1':
        keyword = keyword.decode('base64').decode('utf8')

    mckey = str(binascii.crc32((u'%s%s%s%s%s' % (keyword,start,count,sort,category)).encode('utf8')) & 0xFFFFFFFFL)
    cache = mc.get(mckey)
    if cache:
        print 'bingo', keyword.encode('utf8'), mckey
        return HttpResponse(cache)

    q = search_query.match(keyword)
    if category: q = q.filter(category__eq=binascii.crc32(category)&0xFFFFFFFFL)
    if sort == 'create_time': q = q.order_by('create_time', 'desc')
    if sort == 'length': q = q.order_by('length', 'desc')
    q = q.limit(start, count)
    q2 = search_query.match(keyword).select('category', Count()).group_by('category').named('cats')
    res = q.ask(subqueries=[q2])

    jsp = JsonResponse(res)
    mc.set(mckey, jsp.content)
    return jsp

def json_info(request):
    hashes = request.GET['hashes']
    mckey = str(binascii.crc32(str(hashes)) & 0xFFFFFFFFL)
    cache = mc.get(mckey)
    if cache:
        return HttpResponse(cache)

    res = {}
    for h in hashes.split('-'):
        if len(h) == 40:
            item = Hash.objects.filter(info_hash=h).values()
        else:
            item = Hash.objects.filter(id=h).values()
        res[h] = item[0]
        try:
            filelist = FileList.objects.get(info_hash=res[h]['info_hash'])
            res[h]['files'] = json.loads(filelist.file_list)
        except:
            pass
    jsp = JsonResponse(res)
    mc.set(mckey, jsp.content)
    return jsp

def json_status(request):
    d = {}
    d['hash_total'] = Hash.objects.count()
    reports = StatusReport.objects.order_by('-date')[:30]
    d['reports'] = list(reports.values())
    return JsonResponse(d)

