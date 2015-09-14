# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0033_auto_20150913_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('city', models.ForeignKey(to='travel.City')),
                ('customer', models.ForeignKey(to='travel.Customer')),
            ],
        ),
        migrations.AlterField(
            model_name='cityclick',
            name='num_clicks',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='eventclick',
            name='num_clicks',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='hotelclick',
            name='num_clicks',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='nightlifeclick',
            name='num_clicks',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='outdoorrecreationclick',
            name='num_clicks',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='restaurantclick',
            name='num_clicks',
            field=models.IntegerField(default=0),
        ),
    ]
