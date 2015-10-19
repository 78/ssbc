# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('top', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashlog',
            name='log_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='keywordlog',
            name='log_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
