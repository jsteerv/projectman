# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-06 04:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectman', '0002_auto_20180606_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_client',
            field=models.BooleanField(default=True),
        ),
    ]