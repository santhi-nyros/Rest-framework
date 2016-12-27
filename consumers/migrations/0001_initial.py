# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0001_initial'),
        ('push_notifications', '0002_auto_20160106_0850'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('reg_device', models.ForeignKey(related_name='device', to='push_notifications.GCMDevice')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Consumer_profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25, null=True, blank=True)),
                ('location', models.CharField(max_length=50, null=True, blank=True)),
                ('category', models.ForeignKey(to='providers.Category')),
                ('consumer', models.ForeignKey(to='consumers.Consumer')),
            ],
        ),
    ]
