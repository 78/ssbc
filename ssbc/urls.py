"""ssbc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

import search.views
import web.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/json_search', search.views.json_search),
    url(r'^api/json_info', search.views.json_info),
    url(r'^api/json_status', search.views.json_status),
    url(r'^$', web.views.index, name='index'),
    url(r'^h/(\d{1,10})$', web.views.hash, name='hash'),
    url(r'^hash/(.{40})$', web.views.hash),
    url(r'^info/(.{40})$', web.views.hash_old),
    url(r'^search/(.+?)/(\d*)$', web.views.search_old),
    url(r'^search/(.+?)$', web.views.search),
    url(r'^list/(.+?)/(\d*)$', web.views.search_list, name='list'),
]
