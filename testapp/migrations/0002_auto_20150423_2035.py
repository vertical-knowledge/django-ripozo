# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0001_initial'),
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
