#coding: utf8
import datetime
import re
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(needs_autoescape=True)
def smartcoffee(value, autoescape=True):
    '''Returns input wrapped in HTML <b></b> tags'''
    '''and also detects surrounding autoescape on filter (if any) and escapes '''
    if autoescape:
        value = escape(value)
    result = '<b>%s</b>' % value
    return mark_safe(result)

@register.filter()
def format_time(t):
    if type(t) is datetime.datetime:
        d = t
    else:
        d = datetime.datetime.strptime(t.split('.')[0], '%Y-%m-%dT%H:%M:%S')
    now = datetime.datetime.utcnow()
    dt = now - d
    if dt.days > 365:
        return u'%s年前' % (dt.days / 365)
    elif dt.days > 30:
        return u'%s个月前' % (dt.days/30)
    elif dt.days > 1:
        return u'%s天前' % dt.days
    elif dt.days == 1:
        return u'昨天'
    elif dt.seconds > 3600:
        return mark_safe(u'<span style="color:red;">%s小时前</span>' % (dt.seconds/3600))
    return mark_safe(u'<span style="color:red;">%s分钟前</span>' % (dt.seconds/60))

@register.filter()
def highlight(title, words):
    try:
        for w in words:
            title = re.sub(w, '<span class="highlight">%s</span>' % w, title)
    except:
        pass
    return mark_safe(title)


