from django.shortcuts import render,render_to_response,redirect
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from push_notifications.models import GCMDevice

from providers.models import Provider,Category,Content,Package,Item
from consumers.models import Consumer,Consumer_profile
from consumers.forms import ConsumerForm,ConsumerProfileForm
from consumers.serializers import ConsumerSerializer,ProfileSerializer,GetConsumerSerializer
from providers.serializers import UserSerializer

import simplejson
import json



def consumer_signup(request):
    form = ConsumerForm
    error = ''
    if request.method == 'POST':
        print request.POST
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            consumer = Consumer.objects.filter(email= email).first()
            if consumer:
                error = "Consumer already existed with this mail id"
            else:
                user = User()
                user.username = username
                user.email = email
                user.set_password(password)
                user.save()
                user.groups.add(2)
                consumer = Consumer()
                consumer.user = user
                consumer.email = email
                consumer.save()
                # device = Registered_devices()
                # device.user = consumer
                # device.imei = request.POST['imei']
                # device.device_id = request.POST['device_id']
                # device.save()
                error = "Consumer created successfully"
                return redirect('/')
        except Exception as e:
            error = e
    return render_to_response("consumer_signup.html",{'form':form,'error':error})


def signup(request):
    data ={}
    if request.method == 'POST':
        print request.POST
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            consumer = Consumer.objects.filter(email= email).first()
            if consumer:
                data["result"] = "Consumer already existed with this mail id"
                data['status'] = False
            else:
                user = User()
                user.username = username
                user.email = email
                user.set_password(password)
                user.save()
                user.groups.add(2)
                consumer = Consumer()
                consumer.user = user
                consumer.email = email
                consumer.save()
                # device = Registered_devices()
                # device.user = consumer
                # device.imei = request.POST['imei']
                # device.device_id = request.POST['device_id']
                # device.save()
                # data["result"] = "Consumer created successfully"
                # data['status'] = True
                # return redirect('/')
        except Exception as e:
            error = e
    return HttpResponse(simplejson.dumps(data))

def consumer_profile(request):
    form = ConsumerProfileForm
    status = ''
    consumer = Consumer.objects.filter(email = request.user.email).first()
    profile = Consumer_profile.objects.filter(consumer=consumer).first()
    if request.method == 'POST':
        form = ConsumerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            category = Category.objects.filter(id=request.POST['category']).first()
            if profile:
                profile.first_name = request.POST['first_name']
                profile.last_name = request.POST['last_name']
                profile.category = category
                profile.location = request.POST['location']
                profile.avatar = request.FILES['avatar']
                profile.save()
            else:
                cprofile =Consumer_profile()
                consumer = Consumer.objects.filter(email = request.user.email).first()
                cprofile.consumer = consumer
                cprofile.first_name = request.POST['first_name']
                cprofile.last_name = request.POST['last_name']
                cprofile.avatar = request.FILES['avatar']
                cprofile.category = category
                cprofile.location = request.POST['location']
                cprofile.save()
                status = 'Profile created successfully'
            return redirect('/consumers/view_profile/')
    else:
        if profile:
            print profile.avatar
            data = {
                'first_name':profile.first_name,
                'last_name':profile.last_name,
                'category': profile.category.id,
                'location':profile.location
                }
            file_data = {'avatar':profile.avatar}
            form = ConsumerProfileForm(data, file_data)
    return render_to_response("cprofile.html",{'form':form,'user':request.user,'status':status})


def view_profile(request):
    consumer = Consumer.objects.filter(email = request.user.email).first()
    profile = Consumer_profile.objects.filter(consumer=consumer).first()
    if profile:
        return render_to_response('viewprofile.html',{'user':request.user,'profile':profile})
    else:
        return redirect('/consumers/profile/')


@api_view(['POST','GET'])
def RegistrationAPI(request):
    if request.method == 'GET':
        snippets = Consumer.objects.all()
        serializer = GetConsumerSerializer(snippets, many=True)
        print serializer
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data
        # print data
        # print ""
        # data = json.loads(request.data['req'])
        # device_data = data['device']
        # device_id = device_data['device_id']
        user = User.objects.filter(email = data['email']).first()
        # reg_id = GCMDevice.objects.filter(device_id = device_id).first()
        if user:
            res={'msg':'User already registered with this mail Id.','status':'true'}
            return Response(res)
        else:
            serializer = ConsumerSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                res={'msg':'User registered.','status':'true'}
                return Response(res)
            res = {'msg':serializer.errors, "status":"false"}
            return Response(res)


@api_view(['POST'])
def LoginAPI(request):
    if request.method == 'POST':
        data = json.loads(request.data['req'])
        # data = request.data
        email = data['email']
        password = data['password']
        try:
            consumer = Consumer.objects.filter(email = email).first()
            if consumer:

                user = auth.authenticate(username=consumer.user, password=password)
                auth.login(request, user)
                res={'msg':'Login success','status':'true','user':{'id':user.id,'username':user.username}}
                return Response(res)
            else:
                res={'msg':'User does not exists with these credentials','status':'false'}
                return Response(res)
        except Exception as e:
            res={'e':e, 'status':'false'}
            return Response(res)


@api_view(['POST','GET'])
def ProfileAPI(request):
    if request.method == 'GET':
        snippets = Consumer_profile.objects.all()
        serializer = ProfileSerializer(snippets, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        # data = request.data
        data = json.loads(request.data['req'])
        print data
        consumer = Consumer.objects.filter(user__username = data['username']).first()
        serializer = ProfileSerializer(data={'consumer':consumer.id,'first_name':data['first_name'],'last_name':data['last_name'],'avatar':data['avatar'],'category':data['category'],'location':data['location']})
        if serializer.is_valid():
            serializer.save()
            return Response('Profile created successfully', status=status.HTTP_201_CREATED)
        print serializer.errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def push(request):
    android_devices = GCMDevice.objects.all()
    if android_devices:
        try:
            response = android_devices.send_message("You've got mail")
            print response
            return Response('success')
        except Exception as e:
            return Response(e)
    return Response('No devices')




