#coding: utf8
import traceback

from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import never_cache
from django.http import JsonResponse, HttpResponse

from ssbc import settings
from search.models import Hash, FileList, StatusReport, RecKeywords


@cache_page(600)
def json_search(request):
    keyword = request.GET['keyword']
    start = request.GET.get('start', 0)
    count = request.GET.get('count', 10)
    sort = request.GET.get('sort', '')
    category = request.GET.get('category', '')
    if request.GET.get('base64') == '1':
        keyword = keyword.decode('base64').decode('utf8')
    res = Hash.objects.search(keyword, start, count, category, sort)
    return JsonResponse(res)


@cache_page(600)
def json_info(request):
    hashes = request.GET['hashes']
    try:
        res = Hash.objects.list_with_files(hashes.split('-'))
        j = {'result': res, 'ret': 0}
    except:
        j = {'ret': 1, 'error': traceback.format_exc()}
    return JsonResponse(j)


@cache_page(600)
def json_status(request):
    d = {}
    d['hash_total'] = Hash.objects.count()
    reports = StatusReport.objects.order_by('-date')[:30]
    d['reports'] = list(reports.values())
    return JsonResponse(d)


@never_cache
def json_helper(request):
    kwlist = list(RecKeywords.objects.order_by('-order').values())
    j = {
        'ret': 0,
        'hot_keywords': kwlist,
        'tips': u'手撕包菜搜索助手1.0 <a href="http://www.shousibaocai.com/" target="_blank">磁力搜索</a>',
        'default_option': False,
        'default_url': '', #'http://www.2345.com/?26782',
        'update_url': '',
        'version': '',
    }
    return JsonResponse(j)

