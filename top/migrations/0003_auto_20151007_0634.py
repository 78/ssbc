# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('top', '0002_auto_20151007_0609'),
    ]

    operations = [
        migrations.AddField(
            model_name='hashlog',
            name='ip',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='keywordlog',
            name='ip',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
