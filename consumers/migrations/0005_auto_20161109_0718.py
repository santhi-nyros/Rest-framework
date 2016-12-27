# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumers', '0004_consumer_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registered_devices',
            name='device_id',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='registered_devices',
            name='registration_id',
            field=models.CharField(max_length=500),
        ),
    ]
