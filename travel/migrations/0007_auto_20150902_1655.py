# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0006_auto_20150902_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='first_filter',
            field=models.CharField(default='Outdoor Recreation', verbose_name='First Filter', max_length=50, choices=[('None', 'None'), ('Hotel Price', 'Hotel Price'), ('Restaurant Rating', 'Restaurant Rating'), ('Outdoor Recreation', 'Outdoor Recreation'), ('Events/Concerts', 'Events/Concerts'), ('Night Life', 'Night Life')]),
        ),
    ]
