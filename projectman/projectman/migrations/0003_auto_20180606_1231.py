# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-06 12:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectman', '0002_auto_20180606_0227'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': (('view_project', 'Can see projects'),)},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'permissions': (('view_task', 'Can see task'), ('change_status_task', 'Can change status to task'))},
        ),
    ]
