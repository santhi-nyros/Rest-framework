from __future__ import unicode_literals
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User, Group
# from consumers.models import Consumer_profile
# Create your models here.


class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)
    name = models.CharField(max_length=50,blank=False,null=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name




class Category(models.Model):
    category = models.CharField(max_length=30,blank=False,null=False)

    def __unicode__(self):
        return self.category



class Content(models.Model):
    provider = models.ForeignKey(User, related_name='library')
    category=models.ForeignKey(Category)
    image = models.ImageField(
        upload_to='static/providers/images',
        verbose_name='image',
        blank=True,
        null=True
    )
    video = models.FileField(
        upload_to='static/providers/videos',
        null=False
    )
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.category.category



class Package(models.Model):
    STATUS_CHOICES = (
        ('n', 'Not Published'),
        ('b', 'To be Published'),
        ('p', 'Published')
    )

    provider = models.ForeignKey(User, related_name='packages')
    package_name = models.CharField(max_length=100,blank=True, null=True)
    location = models.CharField(max_length=100,blank=True,null=True)
    business_type = models.CharField(max_length=200,blank=True,null=True)
    scheduled_date = models.DateTimeField(null=True)
    status = models.CharField(default='n', max_length=1, choices=STATUS_CHOICES)

    def __unicode__(self):
        return self.package_name

    def item(package):
        items = Item.objects.filter(package =package)
        return items

    def category(package):
        items = Package.item(package)
        categories = []
        for item in items:
            categories.append(item.item.category)
        categories = sorted(set(categories))
        return categories


class Item(models.Model):
    package = models.ForeignKey(Package)
    item = models.ForeignKey(Content)

    def __str__(self):
        return '%s %s' % (self.item, self.item.id)

