# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from service.models import ProjectConfig

# Create your models here.
@python_2_unicode_compatible
class ChartConfig(models.Model):
    name = models.CharField(max_length=256, null=False)
    class_name = models.CharField(max_length=256, null=False)
    function_name = models.CharField(max_length=256, null=False)
    chart_type = models.CharField(max_length=256, null=False)
    success = models.IntegerField()
    failed = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '结果图表'
        verbose_name_plural = '结果图表'