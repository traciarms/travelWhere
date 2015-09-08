# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0028_auto_20150908_0126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='first_filter',
            new_name='user_filter',
        ),
    ]
