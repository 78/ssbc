#coding: utf8
from django import template
from django.utils.safestring import mark_safe
from search.models import Hash

register = template.Library()

@register.filter()
def hash_name(t):
    h = Hash.objects.filter(id=t).first()
    if h:
        return h.name
    return t

