# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import travel.validators


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0027_auto_20150904_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='zip_code',
            field=models.CharField(null=True, max_length=10, validators=[travel.validators.validate_zip_code]),
        ),
    ]
