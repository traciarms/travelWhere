# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import travel.models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0017_auto_20150903_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='address',
            field=travel.models.TruncatingCharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='loc_city',
            field=travel.models.TruncatingCharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='name',
            field=travel.models.TruncatingCharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='state',
            field=travel.models.TruncatingCharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='url',
            field=travel.models.TruncatingCharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='nightlife',
            name='address',
            field=travel.models.TruncatingCharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='nightlife',
            name='category',
            field=travel.models.TruncatingCharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='nightlife',
            name='loc_city',
            field=travel.models.TruncatingCharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='nightlife',
            name='name',
            field=travel.models.TruncatingCharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='nightlife',
            name='phone',
            field=travel.models.TruncatingCharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='nightlife',
            name='state',
            field=travel.models.TruncatingCharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='nightlife',
            name='url',
            field=travel.models.TruncatingCharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='outdoorrecreation',
            name='category',
            field=travel.models.TruncatingCharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='outdoorrecreation',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='outdoorrecreation',
            name='loc_city',
            field=travel.models.TruncatingCharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='outdoorrecreation',
            name='name',
            field=travel.models.TruncatingCharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='outdoorrecreation',
            name='state',
            field=travel.models.TruncatingCharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='address',
            field=travel.models.TruncatingCharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='category',
            field=travel.models.TruncatingCharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='loc_city',
            field=travel.models.TruncatingCharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='name',
            field=travel.models.TruncatingCharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='phone',
            field=travel.models.TruncatingCharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='state',
            field=travel.models.TruncatingCharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='url',
            field=travel.models.TruncatingCharField(max_length=250, null=True),
        ),
    ]
