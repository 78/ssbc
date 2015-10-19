# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0009_extra_update_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mail_from', models.CharField(max_length=100, verbose_name=b'Mail From')),
                ('subject', models.CharField(max_length=200, verbose_name=b'Subject')),
                ('text', models.TextField(verbose_name=b'Text')),
                ('receive_time', models.DateTimeField(auto_now_add=True)),
                ('is_complaint', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='extra',
            name='blacklist',
        ),
        migrations.RemoveField(
            model_name='extra',
            name='deleted',
        ),
        migrations.AddField(
            model_name='extra',
            name='status',
            field=models.CharField(default='', max_length=20, verbose_name=b'Status', choices=[(b'', b'Normal'), (b'reviewing', b'Reviewing'), (b'disabled', b'Disabled'), (b'deleted', b'Deleted')]),
            preserve_default=False,
        ),
    ]
