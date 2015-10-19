from django.conf.urls import include, url


urlpatterns = [
    url(r'^json_search$', 'search.views.json_search'),
    url(r'^json_info$', 'search.views.json_info'),
    url(r'^json_status$', 'search.views.json_status'),
    url(r'^json_helper$', 'search.views.json_helper'),
    url(r'^post_complaint$', 'search.views.post_complaint'),
]


