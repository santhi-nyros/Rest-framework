from django.contrib import admin
from django.contrib import admin
from django.forms import ModelForm
# Register your models here.
from django.utils.html import format_html
from consumers.models import Consumer,Consumer_profile,Registered_devices

# Register your models here.
admin.site.register(Consumer)
admin.site.register(Registered_devices)
admin.site.register(Consumer_profile)


