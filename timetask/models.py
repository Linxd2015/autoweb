# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from service.models import ProjectConfig
from django.core.urlresolvers import reverse

# Create your models here.
@python_2_unicode_compatible
class TimeTaskConfig(models.Model):
    name = models.CharField('任务名称',max_length=256)
    plan_info = models.ManyToManyField(ProjectConfig, verbose_name=u'自动化项目')
    plan_type = models.ForeignKey('PlanTypeConfig',max_length=256,verbose_name='任务类型')
    plan_time = models.ForeignKey('PlanTimeConfig', max_length=256,verbose_name='具体执行日期')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '计划定时任务'
        verbose_name_plural = '计划定时任务'

@python_2_unicode_compatible
class TotalProjects(models.Model):
    project_type = models.CharField('项目类型',max_length=256)
    project_name = models.CharField('项目名称',max_length=256)

    def __str__(self):
        return self.project_name

@python_2_unicode_compatible
class PlanTastConfig(models.Model):
    name = models.CharField('任务名称(不支持中文)',max_length=256)
    plan_info = models.ManyToManyField(TotalProjects, verbose_name=u'自动化项目')
    plan_type = models.ForeignKey('PlanTypeConfig',max_length=256,verbose_name='任务类型')
    plan_time = models.ForeignKey('PlanTimeConfig', max_length=256,verbose_name='具体执行日期(h)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '计划任务'
        verbose_name_plural = '计划任务'


@python_2_unicode_compatible
class PlanTypeConfig(models.Model):
    name = models.CharField('任务类型',max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '计划类型配置'
        verbose_name_plural = '计划类型配置'





@python_2_unicode_compatible
class PlanTimeConfig(models.Model):
    plan_type = models.ForeignKey('PlanTypeConfig',max_length=256,verbose_name='任务类型')
    name = models.CharField('具体执行日期',max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '计划执行配置'
        verbose_name_plural = '计划执行配置'