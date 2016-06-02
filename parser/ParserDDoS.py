# -*- coding: utf-8 -*-
import datetime
import os
import re
import socket
import sys

import django
import dpkt
from django.core.files import File

from ParserBase import ParserBase
# Модифицированный модуль http из библиотеки dpkt
from dpkt_fixed import http

# Подключение к проекту Django — нужно для доступа к БД посредством Django
sys.path.append(os.path.join(os.path.dirname(__file__), "../sych_server"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sych_server.settings")
django.setup()

from ddos.models import *


class ParserDDoS(ParserBase):
    def parse(self):
        """ Перегруженная функция для работы с трафиком, классифицированным как DDoS-атака """

        # Создаём в средствами ORM Django соответствующий дампу объект в БД
        basename = os.path.basename(self.pcap.name)

        dump, created = Dump.objects.get_or_create(name=basename)
        if created:
            fileobj = File(open(self.pcap.name, 'rb'))
            dump.file = fileobj
            dump.timestamp = datetime.datetime.now()
            dump.save()

        print("Opened " + str(dump))

        counter = 0
        http_counter = 0
        streamDict = {}
        streamID = ''
        stream_counter = 0

        # Цикл попакетной деинкапсуляции дампа средствами dpkt
        for ts, buf in self.pcap:
            counter += 1
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            time = datetime.datetime.fromtimestamp(ts)
            tcp = ip.data

            # Если в TCP пусто, то это не HTTP
            if ip.p not in (dpkt.ip.IP_PROTO_TCP, dpkt.ip.IP_PROTO_UDP):
                continue
            if len(tcp.data) == 0 or (tcp.dport != 80 and tcp.sport != 80):
                continue

            # Определим, запрос это или ответ.
            # Для этого получим первое слово в заголовке
            headers = str(tcp.data).split()

            # Обработка заголовков типа \n\n и пустых заголовоков
            if len(headers) is 0:
                continue
            header = headers[0]

            # TODO: Обработка заголовков настолько огромных, что приходится передавать их по частям,
            # например, когда в адресе содержится длинная строка типа ../../../../../...
            # if (len(headers) < 3) and http.Request.methods.__contains__(header):
            #     os.system("pause")
            #     continue

            try:
                sourceIP = socket.inet_ntoa(ip.src)
                sourcePort = tcp.sport
                destinationIP = socket.inet_ntoa(ip.dst)
                destinationPort = tcp.dport

                # Если это протокол, например, 'HTTP/1.1' то попытаемся распарсить как ответ.
                if header.startswith(http.Response.proto):
                    http_counter += 1
                    http_data = http.Response(tcp.data)
                    tuple = str(destinationIP) + ":" + str(destinationPort) + "->" \
                            + str(sourceIP) + ":" + str(sourcePort)
                    if tuple in streamDict.keys():
                        packet = streamDict[tuple]
                        del streamDict[tuple]
                        # print("Response, stream " + str(streamID) + "\n" + str(http_data))
                        packet.serverResponse = str(http_data).splitlines()[0]
                        if http_data.headers.__contains__('content-type'):
                            packet.serverContentType = http_data.headers['content-type']
                        if http_data.headers.__contains__('content-length'):
                            packet.contentLength = http_data.headers['content-length']

                        packet.save()

                # Иначе — как запрос.
                elif http.Request.methods.__contains__(header):
                    http_counter += 1
                    http_data = http.Request(tcp.data)

                    # print("Request, stream " + str(stream_counter) + "\n" + str(http_data))
                    packet = Packet(timestamp=time, sourceIP=socket.inet_ntoa(ip.src),
                                    sourcePort=tcp.sport, destinationIP=socket.inet_ntoa(ip.dst),
                                    destinationPort=tcp.dport, HTTPMethod=http_data.method, requestURI=http_data.uri,
                                    userAgent=http_data.headers['user-agent'])

                    if http_data.headers.__contains__('content-type'):
                        packet.userContentType = http_data.headers['content-type']
                    if http_data.headers.__contains__('content-length'):
                        packet.contentLength = http_data.headers['content-length']
                    if http_data.headers.__contains__("referer"):
                        packet.referer = http_data.headers['referer']
                    if http_data.headers.__contains__("host"):
                        packet.hostname = http_data.headers['host']

                    # Проверка, интересен ли нам вообще этот пакет
                    if not self.analyze(packet):
                        continue

                    packet.save()
                    packet.dump.add(dump)

                    # Добавляем запрос в библиотеку для поиска соответствующего запроса
                    tuple = str(sourceIP) + ":" + str(sourcePort) + "->" \
                            + str(destinationIP) + ":" + str(destinationPort)
                    stream_counter += 1
                    streamDict[tuple] = packet
                    # Иначе — это не HTTP.

            except Exception, e:
                print("Error: %s" % e)
                print(headers)
        print("HTTP Packets processed: " + str(http_counter))

    def analyze(self, packet):
        # Вес. Используется для задания "разборчивости" фильтра
        weight = 0

        # Проверка User-Agent
        print(packet.userAgent)
        if packet.userAgent.__contains__('Googlebot'):
            return False

        if (len(packet.userAgent) < 12) \
                or re.compile('python|perl|wget').search(packet.userAgent):
            weight += 1
        # Проверка referer
        print(packet.referer)
        if packet.referer == None:
            weight += 1
        # Проверка requestURI
        print(packet.requestURI)
        if packet.requestURI == '/':
            weight += 1

        print(weight)
        if weight > 1:
            return True

        return False


def main():
    parser = ParserDDoS(sys.argv[1])
    parser.open_dump(parser.file_path)
    parser.parse()


if __name__ == "__main__":
    main()
