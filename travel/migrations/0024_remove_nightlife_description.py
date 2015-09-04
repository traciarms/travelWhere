# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0023_auto_20150904_0030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nightlife',
            name='description',
        ),
    ]
