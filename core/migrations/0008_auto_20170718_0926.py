# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20170718_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='companylogos'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, upload_to='profilepics'),
        ),
    ]
