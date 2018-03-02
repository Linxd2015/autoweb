# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import ChartConfig
from django.contrib import admin

# Register your models here.
@admin.register(ChartConfig)
class ChartAdmin(admin.ModelAdmin):
    list_display = ('name',)