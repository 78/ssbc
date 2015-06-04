#coding: utf8
import re
import os

re_blacklist = []

def load_words():
    txt_path = os.path.join(os.path.dirname(__file__), 'politics.txt')
    for line in  open(txt_path, 'r'):
        r = re.compile(line.rstrip('\r\n').decode('utf8'))
        re_blacklist.append(r)
    print 'Loaded words', len(re_blacklist)

def is_sensitive(kw):
    for r in re_blacklist:
        if r.search(kw):
            print kw.encode('utf8'), 'is sensitive'
            return True
    return False

load_words()
is_sensitive(u'习主席')
is_sensitive(u'Test')

