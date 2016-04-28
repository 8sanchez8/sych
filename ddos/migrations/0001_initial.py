# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-28 07:37
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dump',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='upload/')),
                ('name', models.CharField(default=None, max_length=200, null=None)),
                ('timestamp', models.DateTimeField(null=True)),
                ('packets_count', models.PositiveIntegerField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Dumps',
            },
        ),
        migrations.CreateModel(
            name='Packet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(null=True)),
                ('sourceIP', models.GenericIPAddressField(null=True, unpack_ipv4=True)),
                ('sourcePort', models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(65535)])),
                ('destinationIP', models.GenericIPAddressField(null=True, unpack_ipv4=True)),
                ('destinationPort', models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(65535)])),
                ('serverDescription', models.CharField(max_length=200, null=True)),
                ('HTTPMethod', models.CharField(max_length=20, null=True)),
                ('requestURI', models.URLField(null=True)),
                ('hostname', models.CharField(max_length=200, null=True)),
                ('userAgent', models.CharField(max_length=200, null=True)),
                ('referer', models.URLField(null=True)),
                ('userContentType', models.CharField(max_length=200, null=True)),
                ('contentLength', models.PositiveIntegerField(null=True)),
                ('serverResponse', models.CharField(max_length=200, null=True)),
                ('serverContentType', models.CharField(max_length=200, null=True)),
                ('dump', models.ManyToManyField(to='ddos.Dump')),
            ],
            options={
                'verbose_name_plural': 'Packets',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
