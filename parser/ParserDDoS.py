# -*- coding: utf-8 -*-
import datetime
import django
import dpkt
import os
import socket
import sys
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
        dump = Dump(name=self.pcap.name, file=open(self.pcap.name, 'rb'))
        # dump.save()

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
            timestamp = datetime.datetime.fromtimestamp(ts)
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
                continue
            # TODO: Обработка заголовков настолько огромных, что приходится передавать их по частям,
            # например, когда в адресе содержится длинная строка типа ../../../../../...
            # if (len(headers) < 3) and http.Request.methods.__contains__(header):
            #     os.system("pause")
            #     continue

            # Если это протокол, например, 'HTTP/1.1' то попытаемся распарсить как ответ.

            try:
                sourceIP = socket.inet_ntoa(ip.src)
                sourcePort = tcp.sport
                destinationIP = socket.inet_ntoa(ip.dst)
                destinationPort = tcp.dport
                if header.startswith(http.Response.proto):
                    http_counter += 1
                    http_data = http.Response(tcp.data)
                    tuple = str(destinationIP) + ":" + str(destinationPort) + "->" \
                        + str(sourceIP) + ":" + str(sourcePort)
                    if tuple in streamDict.keys():
                        streamID = streamDict[tuple]
                    print "Response, stream " + str(streamID) + "\n" + str(http_data)
                    del streamDict[tuple]
                    # print(time, socket.inet_ntoa(ip.dst), tcp.sport, tcp.dport)
                    # packet = Packet(timestamp=time, sourceIP=socket.inet_ntoa(ip.src), sourcePort=tcp.sport,
                    # destinationIP=socket.inet_ntoa(ip.dst), destinationPort=tcp.dport)
                # Иначе — как запрос.
                elif http.Request.methods.__contains__(header):
                    http_counter += 1
                    http_data = http.Request(tcp.data)
                    tuple = str(sourceIP) + ":" + str(sourcePort) + "->" \
                        + str(destinationIP) + ":" + str(destinationPort)
                    stream_counter += 1
                    streamDict[tuple] = stream_counter
                    print "Request, stream " + str(stream_counter) + "\n" + str(http_data)
                    # print(time, tcp.sport, tcp.dport, __http.method, __http.uri, __http.headers['user-agent'])
                    # packet = Packet(timestamp=time, sourceIP=socket.inet_ntoa(ip.src),
                    # sourcePort=tcp.sport, destinationIP=socket.inet_ntoa(ip.dst), destinationPort=tcp.dport,
                    # HTTPMethod=__http.method, requestURI=__http.uri, userAgent=__http.headers['user-agent'])
                    # Иначе — это не HTTP.
                else:
                    print "Not HTTP"
            except Exception, e:
                print("Error: %s" % e)
                print(headers)
                # upload_to_db(result)
        print("HTTP Packets processed: " + str(http_counter))
        print streamDict


def main():
    parser = ParserDDoS(sys.argv[1])
    parser.open_dump(parser.file_path)
    parser.parse()
    # print "Dump objects: " + str(Dump.objects.all())


if __name__ == "__main__":
    main()
