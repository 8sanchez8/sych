# -*- coding: utf-8 -*-

from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.conf import settings

from models import Report, Dump


class ReportForm(forms.Form):
    class Media:
        js = ()

    class Meta:
        model = Report

    name = forms.CharField(max_length=200, label='Имя отчёта')
    # Дампы, на которых основан отчёт
    dump = forms.ModelMultipleChoiceField(queryset=Dump.objects.all(), label='Дампы, по которым составлен отчёт')

    timeStart = forms.DateField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm:ss",
                                       "pickSeconds": "true", "showTodayButton": "true"}), label='Начало атаки')
    timeEnd = forms.DateField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm:ss",
                                       "pickSeconds": "true", "showTodayButton": "true"}), label='Конец атаки')
    # Продолжительность атаки
    duration = forms.DurationField(required=False, label='Продолжительность атаки')
    # Общее количество атак (пакетов)
    count = forms.IntegerField(required=False, label='Общее количество атак')
    # Количество уникальных IP
    uniqueIP = forms.IntegerField(required=False, label='Количество уникальных IP')
    # Основные страны-участники атаки
    countries = forms.CharField(max_length=200, label='Основные страны-источники')
    # Предполагаемая результативность
    result = forms.CharField(max_length=200, label='Предполагаемая результативность')
    # Предполагаемые управляющие центры
    controlCenters = forms.CharField(max_length=200, label='Предполагаемые управляющие центры')
