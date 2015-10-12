# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rss', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outlet',
            name='updated',
            field=models.DateTimeField(null=True, verbose_name=b'date updated'),
        ),
    ]
