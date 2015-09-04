# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0022_auto_20150904_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nightlife',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
