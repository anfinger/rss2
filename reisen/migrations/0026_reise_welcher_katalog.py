# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-23 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reisen', '0025_auto_20160323_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='reise',
            name='welcher_katalog',
            field=models.CharField(choices=[(b'w', b'Winterkatalog'), (b's', b'Sommerkatalog'), (b'a', b'Winter- und Sommerkatalog'), (b'n', b'nicht zugeordnet')], default=b'n', help_text=b'Hier Katalog f\xc3\xbcr eine Reise w\xc3\xa4hlen.', max_length=1, verbose_name=b'Welcher katalog?'),
        ),
    ]
