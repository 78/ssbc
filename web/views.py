#coding: utf8
import re
import datetime
import sys
import urllib

from django.http import Http404
from django.views.decorators.cache import cache_page
from django.shortcuts import render, redirect

from lib import politics
import workers.metautils
from top.models import KeywordLog
from search.models import RecKeywords, Hash

re_punctuations = re.compile(
    u"。|，|,|！|…|!|《|》|<|>|\"|'|:|：|？|\?|、|\||“|”|‘|’|；|—|（|）|·|\(|\)|　|\.|【|】|『|』|@|&|%|\^|\*|\+|\||<|>|~|`|\[|\]")


@cache_page(600)
def index(request):
    reclist = RecKeywords.objects.order_by('-order')
    return render(request, 'index.html', {'reclist': reclist})


@cache_page(3600*24)
def hash(request, h):
    try:
        res = Hash.objects.list_with_files([h])
        j = res[0]
    except Exception as e:
        raise Http404(str(e))
    d = {'info': j} 
    d['keywords'] = list(set(re_punctuations.sub(u' ', d['info']['name']).split()))
    if 'files' in d['info']:
        d['info']['files'] = [y for y in d['info']['files'] if not y['path'].startswith(u'_')]
        d['info']['files'].sort(key=lambda x:x['length'], reverse=True)
    d['magnet_url'] = 'magnet:?xt=urn:btih:' + d['info']['info_hash'] + '&' + urllib.urlencode({'dn':d['info']['name'].encode('utf8')})
    d['download_url'] = 'http://www.haosou.com/s?' + urllib.urlencode({'ie':'utf-8', 'src': 'ssbc', 'q': d['info']['name'].encode('utf8')})
    return render(request, 'info.html', d)


@cache_page(1800)
def search(request, keyword=None, p=None):
    if not keyword:
        return redirect('/')
    if politics.is_sensitive(keyword):
        return redirect('/?' + urllib.urlencode({'notallow': keyword.encode('utf8')}))
    d = {'keyword': keyword}
    d['words'] = list(set(re_punctuations.sub(u' ', d['keyword']).split()))
    try:
        d['p'] = int(p or request.GET.get('p'))
    except:
        d['p'] = 1
    d['category'] = request.GET.get('c', '')
    d['sort'] = request.GET.get('s', 'create_time')
    d['ps'] = 10
    d['offset'] = d['ps']*(d['p']-1)
    res = Hash.objects.search(keyword, d['offset'], d['ps'], d['category'], d['sort'])
    d.update(res)
    # Fill info
    ids = [str(x['id']) for x in d['result']['items']]
    if ids:
        items = Hash.objects.list_with_files(ids)
        for x in d['result']['items']:
            for y in items:
                if x['id'] == y['id']:
                    x.update(y)
                    x['magnet_url'] = 'magnet:?xt=urn:btih:' + x['info_hash'] + '&' + urllib.urlencode({'dn':x['name'].encode('utf8')})
                    x['maybe_fake'] = x['name'].endswith(u'.rar') or u'BTtiantang.com' in x['name'] or u'liangzijie' in x['name'] or u'720p高清视频' in x['name']
                    if 'files' in x:
                        x['files'] = [z for z in x['files'] if not z['path'].startswith(u'_')][:5]
                        x['files'].sort(key=lambda x:x['length'], reverse=True)
                    else:
                        x['files'] = [{'path': x['name'], 'length': x['length']}]
    # pagination
    w = 10
    total = int(d['result']['meta']['total_found'])
    d['page_max'] = total / d['ps'] if total % d['ps'] == 0 else total/d['ps'] + 1
    d['prev_pages'] = range( max(d['p']-w+min(int(w/2), d['page_max']-d['p']),1), d['p'])
    d['next_pages'] = range( d['p']+1, int(min(d['page_max']+1, max(d['p']-w/2,1) + w )) )
    d['sort_navs'] = [
        {'name': 'By Time', 'value': 'create_time'},
        {'name': 'By Size', 'value': 'length'},
        {'name': 'By Relavance', 'value': 'relavance'},
    ]
    d['cats_navs'] = [{'name': 'All', 'num': total, 'value': ''}]
    d['keyword_logs'] = KeywordLog.objects
    for x in d['cats']['items']:
        v = workers.metautils.get_label_by_crc32(x['category'])
        d['cats_navs'].append({'value': v, 'name': workers.metautils.get_label(v), 'num': x['num']})
        
    return render(request, 'list.html', d)


def hash_old(request, h):
    return redirect('/hash/' + h, permanent=True)


def search_old(request, kw, p):
    return redirect('list', kw, p)


@cache_page(3600*24)
def howto(request):
    return render(request, 'howto.html', {})

