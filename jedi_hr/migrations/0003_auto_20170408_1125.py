# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-08 11:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jedi_hr', '0002_auto_20170408_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='jedi_master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jedi_hr.Jedi'),
        ),
    ]
