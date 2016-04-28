"""sych_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin

from ddos import views as ddos_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', ddos_views.index),
    url(r'^dashboard/', ddos_views.dashboard, name="dashboard"),
    url(r'^admin/', admin.site.urls),
    url(r'^login$', auth_views.login),
    url(r'^logout?$', auth_views.logout),
    url(r'^ddos/', include('ddos.urls')),
    url(r'upload/', ddos_views.upload, name='jfu_upload'),
    url(r'^delete/(?P<pk>\d+)$', ddos_views.upload_delete, name='jfu_delete'),
]
