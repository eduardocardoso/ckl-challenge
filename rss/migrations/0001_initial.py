# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('summary', models.CharField(max_length=400)),
                ('url', models.CharField(unique=True, max_length=250)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('content', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('profile', models.CharField(max_length=100, null=True)),
                ('twitter', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Outlet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=100)),
                ('rss_url', models.CharField(max_length=100, verbose_name=b'rss feed url')),
                ('description', models.CharField(max_length=500, null=True)),
                ('language', models.CharField(max_length=5, null=True)),
                ('updated', models.DateTimeField(verbose_name=b'date updated')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='author',
            name='outlet',
            field=models.ForeignKey(to='rss.Outlet'),
        ),
        migrations.AddField(
            model_name='article',
            name='authors',
            field=models.ManyToManyField(to='rss.Author'),
        ),
        migrations.AddField(
            model_name='article',
            name='outlet',
            field=models.ForeignKey(to='rss.Outlet'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='rss.Tag'),
        ),
    ]
