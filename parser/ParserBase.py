# -*- coding: utf-8 -*-
import dpkt
import os
# Модифицированные библиотеки dpkt
from dpkt_fixed.pcapng import Reader as pcapng_Reader


class ParserBase:
    """ Базовый класс, реализующий парсинг дампов. """

    def __init__(self, file_path=None):
        self.file_path = file_path
        self.valid_extensions = ['tdp', 'pcap', 'pcapng']

    def parse(self):
        raise NotImplementedError()

    def open_dump(self, file_path):
        """ Открывает файл по переданному аргументу, возвращает объект типа dpkt.pcap"""

        if os.path.exists(file_path):
            file = open(file_path, 'rb')
        else:
            raise IOError("Файл не существует")
        extension = os.path.splitext(file_path)[1][1:].strip()
        if extension not in self.valid_extensions:
            raise IOError("Некорректное расширение файла. Это точно дамп?")

        # Файлы типа .tdp зачастую получены командой mergecap, которая по умолчанию
        # сохраняет в формате pcapng. Поэтому проверим заголовок, и если это pcapng,
        # то запустим соответствующий парсер
        header = file.read(4).encode("hex")
        file.seek(0)
        if header == "0a0d0d0a":
            pcap = pcapng_Reader(file)
        elif header == "d4c3b2a1" or header == "a1b2c3d4":
            pcap = dpkt.pcap.Reader(file)
        self.pcap = pcap


