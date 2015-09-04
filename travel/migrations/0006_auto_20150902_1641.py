# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0005_auto_20150831_2220'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=5)),
                ('category', models.CharField(max_length=50)),
                ('venue_name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
                ('url', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=5)),
                ('low_rate', models.FloatField()),
                ('high_rate', models.FloatField()),
                ('rating', models.IntegerField()),
                ('url', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='NightLife',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=5)),
                ('category', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=25)),
                ('description', models.CharField(max_length=250)),
                ('url', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OutdoorRecreation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=5)),
                ('category', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=5)),
                ('category', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=25)),
                ('rating', models.FloatField()),
                ('url', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_filter',
            field=models.CharField(verbose_name='First Filter', default='Out Door Recreation', choices=[('None', 'None'), ('Hotel Price', 'Hotel Price'), ('Restaurant Rating', 'Restaurant Rating'), ('Out Door Recreation', 'Out Door Recreation'), ('Events/Concerts', 'Events/Concerts'), ('Night Life', 'Night Life')], max_length=50),
        ),
    ]
