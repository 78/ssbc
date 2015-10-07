# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_auto_20150912_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('blacklist', models.BooleanField(default=False, verbose_name=b'\xe9\xbb\x91\xe5\x90\x8d\xe5\x8d\x95')),
                ('hash', models.OneToOneField(to='search.Hash')),
            ],
        ),
    ]
