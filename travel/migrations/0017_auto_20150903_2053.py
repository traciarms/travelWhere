# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import travel.models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0016_auto_20150903_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='address',
            field=travel.models.TruncatingCharField(null=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='event',
            name='eventful_id',
            field=travel.models.TruncatingCharField(null=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='event',
            name='loc_city',
            field=travel.models.TruncatingCharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='event',
            name='state',
            field=travel.models.TruncatingCharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=travel.models.TruncatingCharField(null=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='event',
            name='url',
            field=travel.models.TruncatingCharField(null=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue_name',
            field=travel.models.TruncatingCharField(null=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='outdoorrecreation',
            name='category',
            field=models.CharField(null=True, max_length=100),
        ),
    ]
