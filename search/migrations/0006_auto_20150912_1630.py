# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_auto_20150721_0628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reckeywords',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f'),
        ),
    ]
