#coding: utf8
import re
import datetime
import sys
import urllib
import requests
import workers.metautils
from django.http import Http404
from django.shortcuts import render, redirect

from lib import politics

API_URL = 'http://127.0.0.1:8001/api/'
API_HOST = 'www.shousibaocai.com'
re_punctuations = re.compile(
    u"。|，|,|！|…|!|《|》|<|>|\"|'|:|：|？|\?|、|\||“|”|‘|’|；|—|（|）|·|\(|\)|　|\.|【|】|『|』|@|&|%|\^|\*|\+|\||<|>|~|`|\[|\]")
req_session = requests.Session()

# Create your views here.
def index(request):
    reclist = ['哆啦A梦伴我同行', '复仇者联盟2', '速度与激情7','王牌特工']
    d = {'reclist': reclist}
    #return render(request, 'test.html', d)
    return render(request, 'index.html', d)

def hash(request, h):
    qs = {
        'hashes': h,
    }
    url = API_URL + 'json_info?' + urllib.urlencode(qs)
    r = req_session.get(url, headers={'Host':API_HOST})
    try:
        j = r.json()
    except:
        raise Http404(sys.exc_info()[1])
    d = {'info': j[h]} 
    d['keywords'] = list(set(re_punctuations.sub(u' ', d['info']['name']).split()))
    if 'files' in d['info']:
        d['info']['files'] = [y for y in d['info']['files'] if not y['path'].startswith(u'_')]
        d['info']['files'].sort(key=lambda x:x['length'], reverse=True)
    d['magnet_url'] = 'magnet:?xt=urn:btih:' + d['info']['info_hash'] + '&' + urllib.urlencode({'dn':d['info']['name'].encode('utf8')})
    d['download_url'] = 'http://www.so.com/s?' + urllib.urlencode({'ie':'utf-8', 'src': 'ssbc', 'q': d['info']['name'].encode('utf8')})
    return render(request, 'info.html', d)


def search(request, keyword=None, p=None):
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
    # Fetch list
    qs = {
        'keyword': keyword.encode('utf8').encode('base64'),
        'count': d['ps'],
        'start': d['offset'],
        'category': d['category'],
        'sort': d['sort'],
        'base64': 1,
    }
    url = API_URL + 'json_search?' + urllib.urlencode(qs)
    r = req_session.get(url, headers={'Host':API_HOST})
    d.update(r.json())
    # Fill info
    ids = '-'.join([str(x['id']) for x in d['result']['items']])
    if ids:
        qs = {
            'hashes': ids,
        }
        url = API_URL + 'json_info?' + urllib.urlencode(qs)
        r = req_session.get(url, headers={'Host':API_HOST})
        j = r.json()

        for x in d['result']['items']:
            x.update(j[str(x['id'])])
            x['magnet_url'] = 'magnet:?xt=urn:btih:' + x['info_hash'] + '&' + urllib.urlencode({'dn':x['name'].encode('utf8')})
            x['maybe_fake'] = x['name'].endswith(u'.rar')
            if 'files' in x:
                x['files'] = [y for y in x['files'] if not y['path'].startswith(u'_')][:5]
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
        {'name': '按收录时间', 'value': 'create_time'},
        {'name': '按文件大小', 'value': 'length'},
        {'name': '按相关性', 'value': 'relavance'},
    ]
    d['cats_navs'] = [{'name': '全部', 'num': total, 'value': ''}]
    for x in d['cats']['items']:
        v = workers.metautils.get_label_by_crc32(x['category'])
        d['cats_navs'].append({'value': v, 'name': workers.metautils.get_label(v), 'num': x['num']})
        
    return render(request, 'list.html', d)

def hash_old(request, h):
    return redirect('/hash/' + h, permanent=True)

def search_old(request, kw, p):
    return redirect('list', kw, p)

def search_list(request, kw, p):
    return search(request, kw, p)

