# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_auto_20150829_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='first_filter',
            field=models.CharField(max_length=50, default='National Park', verbose_name='First Filter', choices=[('Hotel Price', 'Hotel Price'), ('Restaurant Rating', 'Restaurant Rating'), ('National Park', 'National Parks'), ('Events/Concerts', 'Events/Concerts'), ('Landmarks', 'Landmark')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='second_filter',
            field=models.CharField(max_length=50, default='Events/Concerts', verbose_name='Second Filter', choices=[('Hotel Price', 'Hotel Price'), ('Restaurant Rating', 'Restaurant Rating'), ('National Park', 'National Parks'), ('Events/Concerts', 'Events/Concerts'), ('Landmarks', 'Landmark')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='third_filter',
            field=models.CharField(max_length=50, default='Restaurant Rating', verbose_name='Third Filter', choices=[('Hotel Price', 'Hotel Price'), ('Restaurant Rating', 'Restaurant Rating'), ('National Park', 'National Parks'), ('Events/Concerts', 'Events/Concerts'), ('Landmarks', 'Landmark')]),
        ),
    ]
