# -*- coding: utf-8 -*-
import sys

import dpkt
import psycopg2

import http


class DDoS(object):
    """Working with attacks, classified as DDoS"""

    def __init__(self, filepath, databaseParams):
        self.file = open(filepath, 'rb')
        self.con = None
        self.params = databaseParams

    def parse(self):
        # Файлы типа .tdp зачастую получены командой mergecap, которая по умолчанию
        # сохраняет в формате pcapng. Поэтому проверим заголовок, и если это pcapng,
        # то запустим соответствующий парсер
        header = self.file.read(4).encode("hex")
        self.file.seek(0)

        if header == "0a0d0d0a":
            pcap = dpkt.pcapng.Reader(self.file)
        elif header == "d4c3b2a1" or header == "a1b2c3d4":
            pcap = dpkt.pcap.Reader(self.file)

        # Так выглядит деинкапсуляция в dpkt.
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            tcp = ip.data
            # Если в TCP пусто, то это не HTTP
            if len(tcp.data) == 0:
                continue
            # Определим, запрос это или ответ.
            # Для этого получим первое слово в заголовке
            header = str(tcp.data).split()[0]
            # Если это протокол, например, 'HTTP/1.1' то попытаемся распарсить как ответ.
            if header.startswith(http.Response.proto):
                __http = http.Response(tcp.data)
            # Иначе — как запрос.
            elif http.Request.methods.__contains__(header):
                __http = http.Request(tcp.data)
            # Иначе — это не HTTP.
            else:
                print "not HTTP"
                continue
            print (__http)

        self.file.close()

    def __connectToDB(self):
        try:
            con = psycopg2.connect(**self.params)
            cur = con.cursor()
            cur.execute('SELECT * from ddos_packet')
            test = cur.fetchall()
            print test
            # cur.execute('INSERT INTO test.test(test_column, id) VALUES (%s, %s)', ('{t,e,s,t}', 2))
            # con.commit()
        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
            sys.exit(1)
        finally:
            if con:
                con.close()

    def load(self):
        self.__connectToDB()
        print "Not implemented"
