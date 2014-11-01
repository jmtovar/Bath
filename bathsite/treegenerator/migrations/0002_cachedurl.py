# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('treegenerator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CachedURL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('species', models.CharField(max_length=300)),
                ('database', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=500)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
