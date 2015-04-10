# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_remove_mymodel_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mymodel',
            name='uuid',
        ),
    ]
