"""sample_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from consumers import views
from django.contrib import admin


urlpatterns = [
    url(r'^$', views.RegistrationAPI, name='Registration'),
    url(r'^login/', views.LoginAPI, name='login'),
    url(r'^profile/$', views.ProfileAPI, name="profile"),
    url(r'^view_profile/$', views.view_profile, name="viewprofile"),
    url(r'^push/$', views.push, name="push")
]
