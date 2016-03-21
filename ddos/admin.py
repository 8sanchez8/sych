from django.contrib import admin

from .models import Dump, Analysis

admin.site.register(Dump)
admin.site.register(Analysis)