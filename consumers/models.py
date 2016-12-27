from __future__ import unicode_literals
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User, Group
from push_notifications.models import GCMDevice
from providers.models import Category
# Create your models here.





class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)
    email = models.EmailField(blank=False,unique=True,null=False)

    def __unicode__(self):
        return self.user.username

    def get_profile(consumer):
        profile =  Consumer_profile.objects.filter(consumer=consumer).first()
        return profile

    def get_device(consumer):
        device = Registered_devices.objects.filter(consumer=consumer).first()
        return device

class Registered_devices(models.Model):
    consumer = models.ForeignKey(Consumer)
    device_id = models.CharField(max_length=250,null=False,blank=False)
    registration_id = models.CharField(max_length=500,null=False,blank=False)

    def __unicode__(self):
        return self.device_id




class Consumer_profile(models.Model):
    consumer = models.ForeignKey(Consumer)
    first_name = models.CharField(max_length=25,null=False,blank=False)
    last_name = models.CharField(max_length=25,null=True,blank=True)
    avatar = models.ImageField(
        upload_to='static/consumers/avatars', verbose_name='image', blank=True, null=True)
    category=models.ForeignKey(Category,null=False,blank=False)
    location = models.CharField(max_length=50,null=True,blank=True)

    def __unicode__(self):
        return self.first_name

    def image_img(self):
        if self.avatar:
            return u'<img src="%s" width="50" height="50" />' % self.avatar.url
        else:
            return '(Sin imagen)'
    # image_img.short_description = 'Thumb'
    image_img.allow_tags = True




