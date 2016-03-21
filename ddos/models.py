# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.core.validators import MaxValueValidator
from django.db import models


class Analysis(models.Model):
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
        verbose_name_plural = "Analyzes"

    def __str__(self):
        return str(self.id)


class Dump(models.Model):
    file = models.FileField(upload_to="upload/")
    name = models.CharField(max_length=200, default=file.name)

    # class Dump(models.Model):
    #     #analysis = models.ManyToManyField(Analysis)
    #     file = models.FileField(upload_to='ddos/upload')
    #     dumpName = file.name
    #     slug = models.SlugField(max_length=50, blank=True)
    #
    #     class Meta:
    #         verbose_name_plural = "Dumps"
    #
    #     def __unicode__(self):
    #         return self.file.name
    #
    #     @models.permalink
    #     def get_absolute_url(self):
    #         return ('ddos/upload', )
    #
    #     def save(self, *args, **kwargs):
    #         self.slug = self.file.name
    #         super(Dump, self).save(*args, **kwargs)
    #
    #     def delete(self, *args, **kwargs):
    #         """delete -- Remove to leave file."""
    #         self.file.delete(False)
    #         super(Dump, self).delete(*args, **kwargs)
