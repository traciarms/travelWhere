# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0029_auto_20150908_0147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='user_filter',
            field=models.CharField(verbose_name='Primary Search Filter', default='Outdoor Recreation', max_length=50, choices=[('None', 'None'), ('Hotel Price', 'Hotel Price'), ('Restaurant Rating', 'Restaurant Rating'), ('Outdoor Recreation', 'Outdoor Recreation'), ('Events/Concerts', 'Events/Concerts'), ('Night Life', 'Night Life')]),
        ),
    ]
