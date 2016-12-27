import os

from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

os.environ['DJANGO_SETTINGS_MODULE'] = 'sample_api.settings'

from providers.models import Provider,Category,Content,Package,Item
from consumers.models import Consumer,Consumer_profile
from push_notifications.models import GCMDevice

app = Celery('tasks', broker='redis://localhost:6379')


@app.task()
def send_email(to, package,profiles, html_message=None):
    from_email = 'santhi.nyros@gmail.com'
    subject = 'New Packages'
    # d = Context({ 'package': package, 'items': Package.item(package) })
    # print ""
    # print package
    # print "_______________"*3
    # print Package.item(package)
    print "_______________"*3
    print profiles
    print ""
    # user = User.objects.
    gcm_devices = GCMDevice.objects.all()

    for gcm_device in gcm_devices:
        print gcm_device
        gcm_device.send_message({'message': 'You have a new notification'})

    print "_______________"*3
    # device = GCMDevice.objects.get(registration_id=gcm_reg_id)
    # The first argument will be sent as "message" to the intent extras Bundle
    # Retrieve it with intent.getExtras().getString("message")
    # device.send_message("You've got mail")
    # for item in items:
    #     category = Category.objects.filter(category = item.item).first()
    #     print category
    #     print "++++++++++++++++++++"
    #     print ""
    #     consumers = Consumer_profile.objects.filter(category = category)
    #     print consumers
    #     # print item.item
    #     print ""
    # try:
    #     message = get_template('email.html').render(d)
    #     msg = EmailMessage(subject, message, to=to, from_email=from_email)
    #     msg.content_subtype = 'html'
    #     msg.send()
    #     package = Package.objects.filter(id=package.id).first()
    #     package.status = 'p'
    #     package.save()
    #     print "mail sent"
    #     package
    # except Exception, e:
    #     print "mail error", str(e)
