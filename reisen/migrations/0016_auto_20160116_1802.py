# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-16 17:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reisen', '0015_auto_20160116_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reisepreiszusatz',
            name='preis_id',
        ),
        migrations.RemoveField(
            model_name='reisepreiszusatz',
            name='reisepreis_id',
        ),
        migrations.DeleteModel(
            name='ReisepreisZusatz',
        ),
    ]
