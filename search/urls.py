from django.conf.urls import include, url

from .views import json_status, json_info, json_search, json_helper


urlpatterns = [
    url(r'^json_search', json_search),
    url(r'^json_info', json_info),
    url(r'^json_status', json_status),
    url(r'^json_helper', json_helper),
]


