from django.conf.urls import url

from . import views

app_name = 'ddos'
urlpatterns = [
    # ex: /ddos/5/
    url(r'^(?P<dump_id>[0-9]+)/$', views.analysis, name='analysis'),
    # ex: /ddos/dump_upload
    url(r'^dump/upload', views.dump_upload, name='dump_upload'),
    # ex: /ddos/dump
    url(r'^dump', views.dump_list, name='dump'),

]
