# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0007_auto_20150902_1655'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=5)),
            ],
        ),
        migrations.RenameField(
            model_name='event',
            old_name='city',
            new_name='loc_city',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='city',
            new_name='loc_city',
        ),
        migrations.RenameField(
            model_name='nightlife',
            old_name='city',
            new_name='loc_city',
        ),
        migrations.RenameField(
            model_name='outdoorrecreation',
            old_name='city',
            new_name='loc_city',
        ),
        migrations.RenameField(
            model_name='restaurant',
            old_name='city',
            new_name='loc_city',
        ),
    ]
