#coding: utf8
import re
import hashlib, hmac
import sys
import traceback

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import never_cache
from django.http import JsonResponse, HttpResponse

from django.conf import settings
from search.models import Hash, FileList, StatusReport, RecKeywords, ContactEmail, Extra


@cache_page(600)
def json_search(request):
    keyword = request.GET.get('keyword')
    if not keyword:
        return HttpResponse('keyword needed.')
    start = request.GET.get('start', 0)
    count = request.GET.get('count', 10)
    sort = request.GET.get('sort', '')
    category = request.GET.get('category', '')
    if request.GET.get('base64') == '1':
        keyword = keyword.decode('base64').decode('utf8')
    try:
        res = Hash.objects.search(keyword, int(start), int(count), category, sort)
    except:
        return HttpResponse('Sorry, an error has occurred: %s' % sys.exc_info()[1])
    return JsonResponse(res)


@never_cache
def json_info(request):
    try:
        hashes = request.GET['hashes']
        res = Hash.objects.list_with_files(hashes.split('-'))
        #if request.META.get('HTTP_CF_IPCOUNTRY') == 'US':
        #    raise Exception('403')
        j = {'result': res, 'ret': 0}
    except:
        j = {'ret': 1, 'error': traceback.format_exc()}
    return JsonResponse(j)


@never_cache
def json_status(request):
    d = {}
    d['hash_total'] = Hash.objects.count()
    reports = StatusReport.objects.order_by('-date')[:30]
    d['reports'] = list(reports.values())
    print request.META
    return JsonResponse(d)


@never_cache
def json_helper(request):
    kwlist = list(RecKeywords.objects.order_by('-order').values())
    j = {
        'ret': 0,
        'hot_keywords': kwlist,
        'tips': u'手撕包菜搜索助手1.2  <a href="http://pan.baidu.com/">登录百度云</a>，即可使用云播放在线观看',
        'default_option': True,
        'default_url': settings.HOME_URL,
        'update_url': '',
        'version': '',
    }
    return JsonResponse(j)


def verify(api_key, token, timestamp, signature):
    return signature == hmac.new(
            key=api_key,
            msg='{}{}'.format(timestamp, token),
            digestmod=hashlib.sha256).hexdigest()


@never_cache
@csrf_exempt
def post_complaint(request):
    text = request.POST['stripped-text']
    token = request.POST['token']
    timestamp = request.POST['timestamp']
    signature = request.POST['signature']
    if not verify(settings.MAILGUN_API_KEY, token, timestamp, signature):
        return HttpResponse('Signature failed.')
    is_complaint = False
    if u'opyright' in text or u'版权' in text:
        is_complaint = True
        urls = re.findall(ur'/info/(\d+)', text)
        for pk in urls:
            if not Extra.objects.filter(hash_id=int(pk)).first():
                Extra.objects.create(hash_id=int(pk), status='reviewing')
    ContactEmail.objects.create(subject=request.POST['subject'],
        mail_from=request.POST['from'],
        text=request.POST['stripped-text'],
        is_complaint=is_complaint
    )
    return HttpResponse('Success')



