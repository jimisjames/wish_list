# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-09-24 17:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('belt', '0002_wish_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wish',
            name='date_granted',
        ),
    ]
