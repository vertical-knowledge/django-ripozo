# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('biginteger', models.BigIntegerField()),
                ('boolean', models.BooleanField()),
                ('char', models.CharField(max_length=100)),
                ('csi', models.CommaSeparatedIntegerField(max_length=100)),
                ('date_', models.DateField()),
                ('datetime_', models.DateTimeField()),
                ('decimal_', models.DecimalField(max_digits=5, decimal_places=2)),
                ('duration', models.DurationField()),
                ('email', models.EmailField(max_length=254)),
                ('float_', models.FloatField()),
                ('integer', models.IntegerField()),
                ('ipaddress', models.IPAddressField()),
                ('genericip', models.GenericIPAddressField()),
                ('nullbool', models.NullBooleanField()),
                ('positiveint', models.PositiveIntegerField()),
                ('positivesmallint', models.PositiveSmallIntegerField()),
                ('slug', models.SlugField()),
                ('smallint', models.SmallIntegerField()),
                ('time_', models.TimeField()),
                ('url', models.URLField()),
                ('uuid', models.UUIDField()),
            ],
        ),
    ]
