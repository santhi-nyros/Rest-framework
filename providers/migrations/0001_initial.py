# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to='static/providers/images', null=True, verbose_name='image', blank=True)),
                ('video', models.FileField(upload_to='static/providers/videos')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(to='providers.Category')),
                ('provider', models.ForeignKey(related_name='library', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.ForeignKey(to='providers.Content')),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('package_name', models.CharField(max_length=100, null=True, blank=True)),
                ('location', models.CharField(max_length=100, null=True, blank=True)),
                ('business_type', models.CharField(max_length=200, null=True, blank=True)),
                ('scheduled_date', models.DateTimeField(null=True)),
                ('status', models.CharField(default='n', max_length=1, choices=[('n', 'Not Published'), ('b', 'To be Published'), ('p', 'Published')])),
                ('provider', models.ForeignKey(related_name='packages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='package',
            field=models.ForeignKey(to='providers.Package'),
        ),
    ]
