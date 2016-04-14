# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import MaxValueValidator
from django.db import models


class Dump(models.Model):
    file = models.FileField(upload_to="upload/")
    name = models.CharField(max_length=200, default=file.name, null=file.name)
    timestamp = models.DateTimeField(null=True)
    packets_count = models.PositiveIntegerField(null=True)

    class Meta:
        verbose_name_plural = "Dumps"

    def __str__(self):
        return str(self.name)


class Packet(models.Model):
    # FK для соответствующего дампа
    dump = models.ManyToManyField(Dump)
    # Содержит метку времени получения/отправки пакета.
    timestamp = models.DateTimeField(null=True)
    # Содержит IP-адрес источника пакета.
    sourceIP = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, null=True)
    # sourcePort Содержит порт отправителя.
    sourcePort = models.PositiveIntegerField(validators=[MaxValueValidator(65535)], null=True)
    # destinationIP Содержит IP-адрес получателя.
    destinationIP = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, null=True)
    # destinationPort Содержит порт получателя.
    destinationPort = models.PositiveIntegerField(validators=[MaxValueValidator(65535)], null=True)
    # serverDescription Содержит представление имени сервера в текстовом виде и служит
    # для облегчения визуальной идентификации атакуемого сервера.
    serverDescription = models.CharField(max_length=200, null=True)
    # HTTPMethod Содержит информацию о использованном HTTP-методе (GET, POST, HEAD и прочие).
    HTTPMethod = models.CharField(max_length=20, null=True)
    # requestURI Хранит содержимое HTTP-запроса. URLField
    requestURI = models.URLField(max_length=200, null=True)
    # hostname Доменное имя узла, которому адресован запрос.
    hostname = models.CharField(max_length=200, null=True)
    # userAgent Содержит информацию о клиентском приложении, сформировавшем HTTP-запрос.
    userAgent = models.CharField(max_length=200, null=True)
    # referer Содержит URL источника запроса.
    referer = models.URLField(max_length=200, null=True)
    # userContentType Содержит формат и способ представления данных запроса.
    userContentType = models.CharField(max_length=200, null=True)
    # contentLength Содержит размер содержимого запроса.
    contentLength = models.PositiveIntegerField(null=True)
    # serverResponse Содержит код ответа сервера.
    serverResponse = models.CharField(max_length=200, null=True)
    # serverContentType Содержит формат и способ представления данных ответа.
    serverContentType = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = "Packets"

    def __str__(self):
        return str(self.id)


class Test(models.Model):
    name = models.CharField(max_length=200)
