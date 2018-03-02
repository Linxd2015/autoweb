# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import PlanTastConfig,PlanTypeConfig,PlanTimeConfig
from django.contrib import admin
from AutoTestService.run_main import run_test
import threading


# Register your models here.
class TimeTaskAdmin(admin.ModelAdmin):
    filter_horizontal = ('plan_info',)


@admin.register(PlanTastConfig)
class PlanTaskAdmin(admin.ModelAdmin):
    list_display = ('name','plan_type','plan_time')
    filter_horizontal = ('plan_info',)

    def save_model(self, request, obj, form, change):
        task_name = obj.name
        # plan_type = obj.plan_type.value
        # plan_time = obj.plan_time
        original_name=None
        if change:
            obj_original = self.model.objects.get(pk=obj.pk)
            original_name = obj_original.name
        obj.save()
        t1 = threading.Thread(target=run_test.write_run_task, args=(task_name,original_name))
        t1.setDaemon(True)
        t1.start()


@admin.register(PlanTypeConfig)
class PlanTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(PlanTimeConfig)
class PlanInfoAdmin(admin.ModelAdmin):
    list_display = ('plan_type','name',)
