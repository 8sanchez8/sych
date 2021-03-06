# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-28 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(null=True)),
                ('duration', models.DurationField(null=True)),
                ('count', models.PositiveIntegerField(null=True)),
                ('uniqueIP', models.PositiveIntegerField(null=True)),
                ('countries', models.CharField(max_length=200)),
                ('result', models.CharField(max_length=200)),
                ('controlCenters', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': '\u041e\u0442\u0447\u0451\u0442',
                'verbose_name_plural': '\u041e\u0442\u0447\u0451\u0442\u044b',
            },
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.AlterModelOptions(
            name='dump',
            options={'verbose_name': '\u0414\u0430\u043c\u043f', 'verbose_name_plural': '\u0414\u0430\u043c\u043f\u044b'},
        ),
        migrations.AlterModelOptions(
            name='packet',
            options={'verbose_name': '\u041f\u0430\u043a\u0435\u0442', 'verbose_name_plural': '\u041f\u0430\u043a\u0435\u0442\u044b'},
        ),
        migrations.AddField(
            model_name='report',
            name='dump',
            field=models.ManyToManyField(to='ddos.Dump'),
        ),
    ]
