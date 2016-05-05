# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from jfu.http import upload_receive, UploadResponse, JFUResponse

from models import Dump, Packet
from forms import ReportForm


def index(request):
    context = {}
    if request.user.is_authenticated():
        return redirect('/dashboard', context)
    else:
        return redirect('/login')


@login_required
def dashboard(request):
    context = {}
    return render(request, 'ddos/templates/dashboard.html', context)


@login_required
def dump_list(request):
    dumps = Dump.objects.order_by('-id')
    # TODO: Перенести подсчёт количества пакетов в парсер
    for dump in dumps:
        if dump.packets_count is None:
            dump.packets_count = Packet.objects.filter(dump=dump.id).count()
            dump.save()
    context = {'dump_list': dumps, }
    return render(request, 'ddos/templates/dump/list.html', context)


@login_required
def dump_upload(request):
    context = {}
    return render(request, 'ddos/templates/dump/upload.html', context)

@login_required
def dump_packets(request, dump_id):
    packets = Packet.objects.filter(dump=dump_id)
    return render(request, 'ddos/templates/dump/packets.html', {'packets': packets,})


@require_POST
def upload(request):
    file = upload_receive(request)

    instance = Dump(file=file, name=file.name)
    instance.save()

    basename = os.path.basename(instance.file.path)

    file_dict = {
        'name': basename,
        'size': file.size,

        'url': settings.MEDIA_URL + basename,
        'thumbnailUrl': settings.MEDIA_URL + basename,

        'deleteUrl': reverse('jfu_delete', kwargs={'pk': instance.pk}),
        'deleteType': 'POST',
    }

    return UploadResponse(request, file_dict)


@require_POST
def upload_delete(request, pk):
    success = True
    try:
        instance = Dump.objects.get(pk=pk)
        os.unlink(instance.file.path)
        instance.delete()
    except Dump.DoesNotExist:
        success = False

    return JFUResponse(request, success)


@login_required
def report_list(request):

    return render(request, 'ddos/templates/report/list.html')


@login_required
def report_new(request):

    return render(request, 'ddos/templates/report/new.html', {'form': ReportForm()})
