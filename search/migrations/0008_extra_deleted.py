# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0007_extra'),
    ]

    operations = [
        migrations.AddField(
            model_name='extra',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name=b'\xe5\x88\xa0\xe9\x99\xa4'),
        ),
    ]
