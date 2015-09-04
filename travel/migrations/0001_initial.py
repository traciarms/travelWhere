# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('state', models.CharField(max_length=100, null=True)),
                ('zip_code', models.CharField(max_length=10, null=True)),
                ('distance', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('first_filter', models.CharField(default='National Park', max_length=50, choices=[('Hotel Price', 'Hotel Price'), ('Restaurant Rating', 'Restaurant Rating'), ('National Park', 'National Parks'), ('Events/Concerts', 'Events/Concerts'), ('Landmarks', 'Landmark')], verbose_name='Filter Categories')),
                ('second_filter', models.CharField(default='Events/Concerts', max_length=50, choices=[('Hotel Price', 'Hotel Price'), ('Restaurant Rating', 'Restaurant Rating'), ('National Park', 'National Parks'), ('Events/Concerts', 'Events/Concerts'), ('Landmarks', 'Landmark')], verbose_name='Filter Categories')),
                ('third_filter', models.CharField(default='Restaurant Rating', max_length=50, choices=[('Hotel Price', 'Hotel Price'), ('Restaurant Rating', 'Restaurant Rating'), ('National Park', 'National Parks'), ('Events/Concerts', 'Events/Concerts'), ('Landmarks', 'Landmark')], verbose_name='Filter Categories')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
