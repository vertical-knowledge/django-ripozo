# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0003_remove_mymodel_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mymodel',
            old_name='date_',
            new_name='date_a',
        ),
        migrations.RenameField(
            model_name='mymodel',
            old_name='datetime_',
            new_name='datetime_a',
        ),
        migrations.RenameField(
            model_name='mymodel',
            old_name='decimal_',
            new_name='decimal_a',
        ),
        migrations.RenameField(
            model_name='mymodel',
            old_name='float_',
            new_name='float_a',
        ),
        migrations.RenameField(
            model_name='mymodel',
            old_name='time_',
            new_name='time_a',
        ),
    ]
