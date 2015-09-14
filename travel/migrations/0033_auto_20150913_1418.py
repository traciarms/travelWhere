# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0032_auto_20150910_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityClick',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('num_clicks', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EventClick',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('num_clicks', models.IntegerField()),
                ('customer', models.ForeignKey(to='travel.Customer')),
                ('event', models.ForeignKey(to='travel.Event')),
            ],
        ),
        migrations.CreateModel(
            name='HotelClick',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('num_clicks', models.IntegerField()),
                ('customer', models.ForeignKey(to='travel.Customer')),
                ('hotel', models.ForeignKey(to='travel.Hotel')),
            ],
        ),
        migrations.CreateModel(
            name='NightLifeClick',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('num_clicks', models.IntegerField()),
                ('customer', models.ForeignKey(to='travel.Customer')),
                ('nightlife', models.ForeignKey(to='travel.NightLife')),
            ],
        ),
        migrations.CreateModel(
            name='OutdoorRecreationClick',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('num_clicks', models.IntegerField()),
                ('customer', models.ForeignKey(to='travel.Customer')),
                ('outdoorrecreation', models.ForeignKey(to='travel.OutdoorRecreation')),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantClick',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('num_clicks', models.IntegerField()),
                ('customer', models.ForeignKey(to='travel.Customer')),
                ('restaurant', models.ForeignKey(to='travel.Restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='img_url',
            field=models.CharField(null=True, max_length=250),
        ),
        migrations.AddField(
            model_name='cityclick',
            name='city',
            field=models.ForeignKey(to='travel.City'),
        ),
        migrations.AddField(
            model_name='cityclick',
            name='customer',
            field=models.ForeignKey(to='travel.Customer'),
        ),
    ]
