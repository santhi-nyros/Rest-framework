# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumers', '0002_auto_20161107_1150'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consumer',
            old_name='reg_device',
            new_name='device',
        ),
    ]
