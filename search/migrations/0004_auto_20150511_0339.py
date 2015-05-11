# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_auto_20150511_0316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hash',
            name='tagged',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
