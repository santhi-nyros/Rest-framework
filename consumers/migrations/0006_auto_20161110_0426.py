# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('consumers', '0005_auto_20161109_0718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumer',
            name='device',
        ),
        migrations.AddField(
            model_name='registered_devices',
            name='consumer',
            field=models.ForeignKey(default=345678, to='consumers.Consumer'),
            preserve_default=False,
        ),
    ]
