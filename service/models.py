# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from DjangoUeditor.models import UEditorField
from django.core.urlresolvers import reverse
from autoweb import settings

# Create your models here.


@python_2_unicode_compatible
class Column(models.Model):
    name = models.CharField('栏目名称', max_length=256)
    slug = models.CharField('栏目网址', max_length=256, db_index=True)
    intro = models.TextField('栏目简介', default='')
    nav_display = models.BooleanField('导航显示', default=False)
    home_display = models.BooleanField('首页显示', default=False)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('column',args=(self.slug,))
    class Meta:
        verbose_name = '栏目'
        verbose_name_plural = '栏目'
        ordering = ['name']


@python_2_unicode_compatible
class Article(models.Model):
    column = models.ManyToManyField(Column, verbose_name='归属栏目')
    title = models.CharField('标题', max_length=256)
    slug = models.CharField('网址', max_length=256, db_index=True)
    author = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='作者')
    # content = models.TextField('内容', default='', blank=True)
    #仅修改 content 字段
    content = UEditorField('内容', height=300, width=1000,
        default=u'', blank=True, imagePath="uploads/images/",
        toolbars='besttome', filePath='uploads/files/')
    published = models.BooleanField('正是发布', default=True)
    pub_date = models.DateTimeField('发表时间',auto_now_add=True,editable=True)
    update_time = models.DateTimeField('更新时间',auto_now_add=True,null=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', args=(self.pk,self.slug))
    class Meta:
        verbose_name='教程'
        verbose_name_plural= '教程'


@python_2_unicode_compatible
class AutoTest(models.Model):
    # project_name = models.CharField('接口项目',max_length=256,null=False)
    # class_name = models.CharField('接口类', max_length=256,null=False)
    project_name = models.ForeignKey('ProjectConfig',verbose_name='项目',null=False)
    class_name = models.ForeignKey('ObjectConfig',verbose_name='类',null=False)
    name = models.CharField('接口名称',max_length=256,null=False)
    is_run = models.BooleanField('状态',default=False)
    pre_data_file = models.FileField('数据文件', upload_to='uploads/script/',null=True,blank=True)
    script_path = models.FileField('用例文件',upload_to='uploads/script/',null=True,blank=True)
    schedule = models.CharField('进度',max_length=256,null=True,blank=True)
    result = models.FileField('执行结果', upload_to='uploads/script/')
    creater = models.CharField('创建人', max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例管理'
        verbose_name_plural = '用例管理'
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
class ObjectConfig(models.Model):
    name = models.CharField('类',max_length=256,null=False)
    project = models.ForeignKey('ProjectConfig',verbose_name='所属项目',null=False)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '类配置'
        verbose_name_plural = '类配置'







