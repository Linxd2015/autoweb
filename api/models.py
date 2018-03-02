# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
# from django.utils.html import format_html

# Create your models here.


@python_2_unicode_compatible
class ApiTest(models.Model):
    project_name = models.ForeignKey('ProjectConfig',verbose_name='项目',null=False)
    class_name = models.ForeignKey('VersionConfig',verbose_name='版本',null=False)
    name = models.CharField('接口名称',max_length=256,null=False)
    is_run = models.BooleanField('状态',default=False)
    pre_data_file = models.FileField('数据文件', upload_to='uploads/script/',null=True,blank=True)
    script_path = models.FileField('用例文件',upload_to='uploads/script/',null=True,blank=True)
    schedule = models.CharField('进度',max_length=256,null=True,blank=True)
    result = models.FileField('执行结果', upload_to='uploads/script/')
    creater = models.CharField('创建人',max_length=256,null=True,blank=True)

    def __str__(self):
        return self.name

    # def colored_name(self):
    #     if self.schedule == '100%':
    #         color_code ='green'
    #     else:color_code = 'red'
    #     # self.color_code = 'green'
    #     return format_html(
    #         '<span style="color: #{};">{} {}</span>',
    #         color_code,
    #         self.name,
    #     )
    class Meta:
        verbose_name = 'API用例管理'
        verbose_name_plural = 'API用例管理'
        ordering = ['name']


@python_2_unicode_compatible
class ProjectConfig(models.Model):
    name = models.CharField('接口项目',max_length=256,null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目配置'
        verbose_name_plural = '项目配置'


@python_2_unicode_compatible
class VersionConfig(models.Model):
    name = models.CharField('版本',max_length=256,null=False)
    project = models.ForeignKey('ProjectConfig',verbose_name='所属项目',null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '版本配置'
        verbose_name_plural = '版本配置'
