# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-07 00:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectman', '0004_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_manager',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='projectman.ProjectmanagerProfile'),
            preserve_default=False,
        ),
    ]