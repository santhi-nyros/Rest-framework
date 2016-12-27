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
from providers import views
from django.contrib import admin

router = routers.DefaultRouter()
# router.register(r'api/users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
# router.register('category',views.GetCategories)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^consumers/', include('consumers.urls')),

    url(r'^api/users', views.UserViewSet, name='users'),
    url(r'^api/categories', views.GetCategories, name='categories'),
    # url(r'^', views.ProviderLogin, name='login'),
    url(r'^', views.home, name='home'),
    url(r'^library/$', views.library_view, name='library'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^create_package/$', views.Create_package, name='create_package'),
    url(r'^package_view/$', views.package_view, name='package_view'),
    url(r'^view_pack/(?P<pid>[A-Za-z0-9\w @%._-]+)/$', views.pack_items, name='view_pack'),
    # url(r'^', include(router.urls)),
    # url(r'^publish/$', views.publish, name="publish"),
    url(r'^admin/', admin.site.urls),
    # url(r'^$', 'mobapp.views.index'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]

