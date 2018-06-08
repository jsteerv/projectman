# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-07 06:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectman', '0004_merge_20180606_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChildTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('complete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='state',
            field=models.IntegerField(choices=[(1, 'Done'), (2, 'In-progess'), (3, 'To-do')], default=3),
        ),
        migrations.AddField(
            model_name='childtask',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_child', to='projectman.Task'),
        ),
    ]
