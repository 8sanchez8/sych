from django.conf.urls import url

from . import views

app_name = 'ddos'
urlpatterns = [
    # ex: /ddos/5/
    url(r'^(?P<dump_id>[0-9]+)/$', views.dump_packets, name='analysis'),
    # ex: /ddos/dump_upload
    url(r'^dump/upload', views.dump_upload, name='dump_upload'),
    # ex: /ddos/dump
    url(r'^dump', views.dump_list, name='dump'),
    # ex: /ddos/report/new
    url(r'^report/new', views.report_new, name='report_new'),
    # ex: /ddos/report
    url(r'^report', views.report_list, name='report_list'),

]
