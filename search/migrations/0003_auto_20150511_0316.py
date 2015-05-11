# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_filelist_hash_statusreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statusreport',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]
