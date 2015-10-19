# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HashLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_time', models.DateTimeField(auto_now_add=True)),
                ('hash_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='KeywordLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_time', models.DateTimeField(auto_now_add=True)),
                ('keyword', models.CharField(max_length=100)),
            ],
        ),
    ]
