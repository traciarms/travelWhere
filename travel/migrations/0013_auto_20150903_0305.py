# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0012_auto_20150903_0303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='address',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='address',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='url',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='nightlife',
            name='address',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='nightlife',
            name='category',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='nightlife',
            name='description',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='nightlife',
            name='phone',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='nightlife',
            name='url',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='outdoorrecreation',
            name='category',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='outdoorrecreation',
            name='description',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='address',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='category',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='phone',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='url',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
