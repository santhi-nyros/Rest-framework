# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registered_devices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_id', models.CharField(unique=True, max_length=250)),
                ('registration_id', models.CharField(unique=True, max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='consumer',
            name='reg_device',
            field=models.ForeignKey(to='consumers.Registered_devices'),
        ),
    ]
