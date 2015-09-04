# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0018_auto_20150903_2058'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='outdoorrecreation',
            unique_together=set([('name', 'loc_city', 'state')]),
        ),
    ]
