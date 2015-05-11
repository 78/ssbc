#coding: utf8
import os

def get_label(name):
    cats = {
        u'video': u'视频',
        u'image': u'图片',
        u'document': u'书籍',
        u'music': u'音乐',
        u'package': u'压缩',
        u'software': u'软件',
    }
    if name in cats:
        return cats[name]
    return u'其它'

def get_extension(name):
    return os.path.splitext(name)[1]

def get_category(ext):
    ext = ext + '.'
    cats = {
        u'video': '.avi.mp4.rmvb.m2ts.wmv.mkv.flv.qmv.rm.mov.vob.asf.3gp.mpg.mpeg.m4v.f4v.',
        u'image': '.jpg.bmp.jpeg.png.gif.tiff.',
        u'document': '.pdf.isz.chm.txt.epub.bc!.doc.ppt.',
        u'music': '.mp3.ape.wav.dts.mdf.flac.',
        u'package': '.zip.rar.7z.tar.gz.iso.dmg.pkg.',
        u'software': '.exe.app.msi.apk.'
    }
    for k, v in cats.iteritems():
        if ext in v:
            return k
    return u'other'

def get_detail(y):
    if y.get('files'):
        y['files'] = [z for z in y['files'] if not z['path'].startswith('_')]
    else:
        y['files'] = [{'path': y['name'], 'length': y['length']}]
    y['files'].sort(key=lambda z:z['length'], reverse=True)
    bigfname = y['files'][0]['path']
    ext = get_extension(bigfname).lower()
    y['category'] = get_category(ext)
    y['extension'] = ext


