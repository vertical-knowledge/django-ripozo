# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ManyToOne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('many_value', models.CharField(max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('biginteger', models.BigIntegerField()),
                ('boolean', models.BooleanField(default=False)),
                ('char', models.CharField(max_length=100)),
                ('csi', models.CommaSeparatedIntegerField(max_length=100)),
                ('date_a', models.DateField()),
                ('datetime_a', models.DateTimeField()),
                ('decimal_a', models.DecimalField(max_digits=5, decimal_places=2)),
                ('email', models.EmailField(max_length=254)),
                ('float_a', models.FloatField()),
                ('integer', models.IntegerField()),
                ('ipaddress', models.IPAddressField()),
                ('genericip', models.GenericIPAddressField()),
                ('nullbool', models.NullBooleanField()),
                ('positiveint', models.PositiveIntegerField()),
                ('positivesmallint', models.PositiveSmallIntegerField()),
                ('slug', models.SlugField()),
                ('smallint', models.SmallIntegerField()),
                ('time_a', models.TimeField()),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='OneToMany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('one_value', models.CharField(max_length=63)),
            ],
        ),
        migrations.AddField(
            model_name='manytoone',
            name='one',
            field=models.ForeignKey(related_name='manies', to='testapp.OneToMany'),
        ),
    ]
