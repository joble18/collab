# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-28 11:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_companyprofile_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logo/'),
        ),
    ]