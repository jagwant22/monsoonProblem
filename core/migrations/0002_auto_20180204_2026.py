# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-04 20:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdfuploadmodel',
            name='query_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='pdfuploadmodel',
            name='query_year',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
