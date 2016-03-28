# -*- coding: utf-8 -*-
import datetime
import os
import sys

import django
import dpkt
from django.core.files import File

import http

sys.path.append(os.path.join(os.path.dirname(__file__), "../sych_server"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sych_server.settings")
django.setup()

from ddos.models import *


def parse():
    file_path = sys.argv[1]
    print file_path
    f = open(file_path, 'rb')

    # Файлы типа .tdp зачастую получены командой mergecap, которая по умолчанию
    # сохраняет в формате pcapng. Поэтому проверим заголовок, и если это pcapng,
    # то запустим соответствующий парсер
    header = f.read(4).encode("hex")
    f.seek(0)

    f_dj = open(sys.argv[1], 'rb')
    django_file = File(f_dj)
    dump = Dump(name=f.name, file=django_file)
    # dump.save()

    if header == "0a0d0d0a":
        pcap = dpkt.pcapng.Reader(f)
    elif header == "d4c3b2a1" or header == "a1b2c3d4":
        pcap = dpkt.pcap.Reader(f)

    counter = 0
    http_counter = 0
    # Так выглядит деинкапсуляция в dpkt.
    for ts, buf in pcap:
        counter += 1
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        tcp = ip.data
        # Если в TCP пусто, то это не HTTP
        if len(tcp.data) == 0 or (tcp.dport != 80 and tcp.sport != 80):
            continue

        # Определим, запрос это или ответ.
        # Для этого получим первое слово в заголовке
        headers = str(tcp.data).split()
        header = headers[0]

        # Обработка заголовков типа \n\n и пустых заголовоков
        if len(headers) is 0:
            print "no headers"
            continue
        # Обработка заголовков настолько огромных, что приходится передавать их по частям,
        # например, когда в адресе содержится длинная строка типа ../../../../../...
        # if (len(headers) < 3) and http.Request.methods.__contains__(header):
        #     os.system("pause")
        #     continue

        # Если это протокол, например, 'HTTP/1.1' то попытаемся распарсить как ответ.
        time = datetime.datetime.fromtimestamp(ts)
        try:
            if header.startswith(http.Response.proto):
                http_counter += 1
                __http = http.Response(tcp.data)
                print "Response\n" + str(__http)
                # print(time, socket.inet_ntoa(ip.dst), tcp.sport, tcp.dport)
                # packet = Packet(timestamp=time, sourceIP=socket.inet_ntoa(ip.src), sourcePort=tcp.sport,
                # destinationIP=socket.inet_ntoa(ip.dst), destinationPort=tcp.dport)
            # Иначе — как запрос.
            elif http.Request.methods.__contains__(header):
                http_counter += 1
                __http = http.Request(tcp.data)
                print "Request\n" + str(__http)
                # print(time, tcp.sport, tcp.dport, __http.method, __http.uri, __http.headers['user-agent'])
                # packet = Packet(timestamp=time, sourceIP=socket.inet_ntoa(ip.src),
                # sourcePort=tcp.sport, destinationIP=socket.inet_ntoa(ip.dst), destinationPort=tcp.dport,
                # HTTPMethod=__http.method, requestURI=__http.uri, userAgent=__http.headers['user-agent'])
            # Иначе — это не HTTP.
            else:
                print "not HTTP"
                print "Progress: " + str(counter)
                continue
                # packet.save()
        except Exception, e:
            print "Error %s" % e
            print headers

    f.close()
    print "End"


def main():
    parse()
    # print "Dump objects: " + str(Dump.objects.all())


if __name__ == "__main__":
    main()
