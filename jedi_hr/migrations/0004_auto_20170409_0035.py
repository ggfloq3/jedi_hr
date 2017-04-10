# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-09 00:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jedi_hr', '0003_auto_20170408_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedi_hr.Candidate')),
            ],
        ),
        migrations.RenameModel(
            old_name='PadawanQuiz',
            new_name='Quiz',
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='jedi_hr.Quiz'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidateanswer',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedi_hr.Quiz'),
        ),
    ]