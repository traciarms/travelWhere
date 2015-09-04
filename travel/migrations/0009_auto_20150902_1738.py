# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0008_auto_20150902_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.ForeignKey(to='travel.City', null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='city',
            field=models.ForeignKey(to='travel.City', null=True),
        ),
        migrations.AddField(
            model_name='nightlife',
            name='city',
            field=models.ForeignKey(to='travel.City', null=True),
        ),
        migrations.AddField(
            model_name='outdoorrecreation',
            name='city',
            field=models.ForeignKey(to='travel.City', null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='city',
            field=models.ForeignKey(to='travel.City', null=True),
        ),
    ]
