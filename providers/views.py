import datetime
import ast
import json

from django.shortcuts import render,render_to_response,redirect
from django.template import RequestContext
# Create your views here.
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from providers.serializers import (
        UserSerializer,
        GroupSerializer,
        ProviderSerializer,
        CategorySerializer
    )
from providers.models import Provider,Category,Content,Package,Item
from consumers.models import Consumer
from providers.forms import LoginForm,PackageForm
from consumers.forms import ConsumerProfileForm
from .tasks import send_email


def home(request):
    user = request.user
    group = user.groups.all()
    # if request.user.is_anonymous():
    #     return redirect('/login')
    # elif request.user.is_superuser:
    #     return redirect('/admin')
    # elif group[0].name == 'Consumers':
    #     form = ConsumerProfileForm
    #     return render_to_response("cindex.html",{'user':user,'form':form})
    return render_to_response("index.html",{'user':user})



def ProviderLogin(request):
    form = LoginForm()
    error = "User does not exists with these credentials"
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.filter(username= request.POST['username']).first()
                if user:
                    user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
                    auth.login(request, user)
                    if user.is_superuser:
                        return redirect('/admin')
                    else:
                        return redirect('/home')
            except User.DoesNotExist:
                error = "User does not exists with these credentials"
            except Exception as e:
                error = "User name/ password not correct"
                pass
    else:
        if request.user.is_anonymous():
            pass
        # else:
        #     return redirect('/home')
        # error = ""
    return render_to_response("login.html",{'form':form,'error':error})



@login_required
def logout_view(request):
    auth.logout(request)
    return redirect('/')


@login_required
def library_view(request):
    form = PackageForm
    data = Content.objects.filter(provider=request.user)
    return render_to_response("library.html",{'data':data,'user':request.user,'form':form})

@login_required
def Create_package(request):
    form = PackageForm
    data = Content.objects.filter(provider=request.user)
    if request.method == 'POST':
        try:
            pack_name = request.POST['pack_name']
            location = request.POST['location']
            business_type = request.POST['business_type']
            items = request.POST['items']
            package = Package()
            package.provider = request.user
            package.package_name = pack_name
            package.location = location
            package.business_type = business_type
            package.save()
            for i in ast.literal_eval(items):
                i = Content.objects.filter(id=i).first()
                item = Item()
                item.package = package
                item.item = i
                item.save()
            return redirect('/package_view')
        except Exception as e:
            print e
    return render_to_response("library.html",{'data':data,'user':request.user,'form':form})



@login_required
def package_view(request):
    packages = Package.objects.filter(provider=request.user)
    return render_to_response("packages.html",{'packages':packages,'user':request.user})

@login_required
def pack_items(request,pid):
    package = Package.objects.filter(id=pid).first()
    packs = Package.item(package)
    return render_to_response("pack_details.html",{'package':package,'user':request.user,'packs':packs})


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



@api_view(['GET',])
def hello(request):
    data = {'msg':'Hello world!!','status':True}
    text = json.dumps(data)
    return HttpResponse(text)

@api_view(['GET', 'POST'])
def UserViewSet(request):
    if request.method == 'GET':
        snippets = User.objects.all()
        serializer = UserSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # data = json.loads(request.data['req'])
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def GetCategories(request):
    queryset = Category.objects.all()
    serializer = CategorySerializer(queryset, many=True)
    res = {'categories':serializer.data}
    return Response(res)




# def signup(request):
#     data = User.objects.all()
#     if request.POST:
#         user = User.objects.create_user(
#                 username = serializer.init_data['username'],
#                 email = serializer.init_data['email'],
#                 password = serializer.init_data['password']
#             )


# def articles(request, format=None):
#     data= {'articles': Article.objects.all() }
#     return Response(data, template_name='articles.html')
