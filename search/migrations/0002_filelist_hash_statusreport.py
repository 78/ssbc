# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileList',
            fields=[
                ('info_hash', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('file_list', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Hash',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('info_hash', models.CharField(unique=True, max_length=40)),
                ('category', models.CharField(max_length=20)),
                ('data_hash', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=255)),
                ('extension', models.CharField(max_length=20)),
                ('classified', models.BooleanField(default=False)),
                ('source_ip', models.CharField(max_length=20, null=True)),
                ('tagged', models.BooleanField(default=False)),
                ('length', models.BigIntegerField()),
                ('create_time', models.DateTimeField()),
                ('last_seen', models.DateTimeField()),
                ('requests', models.PositiveIntegerField()),
                ('comment', models.CharField(max_length=255, null=True)),
                ('creator', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatusReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('new_hashes', models.IntegerField()),
                ('total_requests', models.IntegerField()),
                ('valid_requests', models.IntegerField()),
            ],
        ),
    ]
