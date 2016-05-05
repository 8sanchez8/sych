# -*- coding: utf-8 -*-

import os
import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    for dump in dumps.iterator():
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
    rows = request.GET.get('rows', 25)
    packets_list = Packet.objects.filter(dump=dump_id)
    paginator = Paginator(packets_list, rows)
    page = request.GET.get('page', 1)
    try:
        packets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        packets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        packets = paginator.page(paginator.num_pages)
    return render(request, 'ddos/templates/dump/packets.html', {'packets': packets, 'page': page, 'rows': rows})


@require_POST
def upload(request):
    file = upload_receive(request)

    instance = Dump(file=file, name=file.name, timestamp=datetime.datetime.now())
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
