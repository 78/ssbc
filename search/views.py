from django.shortcuts import render
from ssbc import settings
from django.http import JsonResponse, HttpResponse
from search.models import Hash, FileList
from sphinxit.core.helpers import BaseSearchConfig
from sphinxit.core.processor import Search
import binascii
import json
import memcache

class SphinxitConfig(BaseSearchConfig):
    WITH_STATUS = False
search_query = Search(indexes=['rt_main'], config=SphinxitConfig)
mc = memcache.Client(['127.0.0.1:11211'],debug=0)

# Create your views here.
def json_search(request):
    keyword = request.GET['keyword']
    start = request.GET.get('start', 0)
    count = request.GET.get('count', 10)
    if request.GET.get('base64') == '1':
        keyword = keyword.decode('base64').decode('utf8')

    mckey = str(binascii.crc32((u'%s%s%s' % (keyword,start,count)).encode('utf8')) & 0xFFFFFFFFL)
    cache = mc.get(mckey)
    if cache:
        print 'bingo', keyword.encode('utf8'), mckey
        return HttpResponse(cache)

    q = search_query.match(keyword).limit(start, count).order_by('create_time', 'desc')
    res = q.ask()

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


