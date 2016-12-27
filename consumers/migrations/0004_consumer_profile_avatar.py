# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumers', '0003_auto_20161107_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumer_profile',
            name='avatar',
            field=models.ImageField(upload_to='static/consumers/avatars', null=True, verbose_name='image', blank=True),
        ),
    ]
