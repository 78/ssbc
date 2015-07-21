# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_auto_20150511_0339'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecKeywords',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=20, verbose_name=b'\xe6\x8e\xa8\xe8\x8d\x90\xe5\x85\xb3\xe9\x94\xae\xe8\xaf\x8d')),
                ('order', models.PositiveIntegerField(verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f')),
            ],
        ),
        migrations.AlterField(
            model_name='filelist',
            name='file_list',
            field=models.TextField(verbose_name=b'JSON\xe6\xa0\xbc\xe5\xbc\x8f\xe7\x9a\x84\xe6\x96\x87\xe4\xbb\xb6\xe5\x88\x97\xe8\xa1\xa8'),
        ),
        migrations.AlterField(
            model_name='hash',
            name='category',
            field=models.CharField(max_length=20, verbose_name=b'\xe7\xb1\xbb\xe5\x88\xab'),
        ),
        migrations.AlterField(
            model_name='hash',
            name='classified',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\x88\x86\xe7\xb1\xbb'),
        ),
        migrations.AlterField(
            model_name='hash',
            name='create_time',
            field=models.DateTimeField(verbose_name=b'\xe5\x85\xa5\xe5\xba\x93\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='hash',
            name='data_hash',
            field=models.CharField(max_length=32, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9\xe7\xad\xbe\xe5\x90\x8d'),
        ),
        migrations.AlterField(
            model_name='hash',
            name='extension',
            field=models.CharField(max_length=20, verbose_name=b'\xe6\x89\xa9\xe5\xb1\x95\xe5\x90\x8d'),
        ),
        migrations.AlterField(
            model_name='hash',
            name='last_seen',
            field=models.DateTimeField(verbose_name=b'\xe4\xb8\x8a\xe6\xac\xa1\xe8\xaf\xb7\xe6\xb1\x82\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='hash',
            name='length',
            field=models.BigIntegerField(verbose_name=b'\xe6\x96\x87\xe4\xbb\xb6\xe5\xa4\xa7\xe5\xb0\x8f'),
        ),
        migrations.AlterField(
            model_name='hash',
            name='name',
            field=models.CharField(max_length=255, verbose_name=b'\xe8\xb5\x84\xe6\xba\x90\xe5\x90\x8d\xe7\xa7\xb0'),
        ),
        migrations.AlterField(
            model_name='hash',
            name='requests',
            field=models.PositiveIntegerField(verbose_name=b'\xe8\xaf\xb7\xe6\xb1\x82\xe6\xac\xa1\xe6\x95\xb0'),
        ),
        migrations.AlterField(
            model_name='hash',
            name='source_ip',
            field=models.CharField(max_length=20, null=True, verbose_name=b'\xe6\x9d\xa5\xe6\xba\x90IP'),
        ),
        migrations.AlterField(
            model_name='hash',
            name='tagged',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe7\xb4\xa2\xe5\xbc\x95'),
        ),
        migrations.AlterField(
            model_name='statusreport',
            name='date',
            field=models.DateField(unique=True, verbose_name=b'\xe6\x97\xa5\xe6\x9c\x9f'),
        ),
        migrations.AlterField(
            model_name='statusreport',
            name='new_hashes',
            field=models.IntegerField(verbose_name=b'\xe6\x96\xb0\xe5\xa2\x9e\xe8\xb5\x84\xe6\xba\x90'),
        ),
    ]
