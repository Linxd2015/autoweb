# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import ApiTest,ProjectConfig,VersionConfig
from AutoTestService.run_main.run_test import *
from autoweb.settings import *

# Register your models here.


@admin.register(ApiTest)
class ApiTestAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'class_name', 'name', 'is_run', 'schedule', 'result','pre_data_file',
                    'script_path')
    search_fields = ('project_name__name', 'class_name__name', 'name')
    list_filter = ('project_name__name', 'class_name__name','creater')
    actions = ['make_story_public','clear_action']
    list_display_links = ('project_name','class_name','name')

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('schedule','result','creater')
        form = super(ApiTestAdmin, self).get_form(request,obj,**kwargs)
        return form

    def clear_action(self,request,queryset):
        """
        执行前的清理操作
        :param request:
        :param queryset:
        :return:
        """
        full_path = request.path.split('/')
        clear_run_actions(queryset, {"app_name": full_path[2], "model_name": full_path[3]})
        # clear_run_actions(queryset)

    def make_story_public(self, request, queryset):
        """
        点击执行的逻辑
        :param request:
        :param queryset:
        :return:
        """
        full_path = request.path.split('/')
        # print request.path
        # print full_path[2],full_path[3]
        run_test(queryset,"api",{"app_name":full_path[2],"model_name":full_path[3]})
        queryset.update(is_run=1)
        # ddd = queryset[0]
        # aa = queryset.filter(name=queryset[0])
        # print aa[0].project_name,aa[0].class_name,aa[0].name
        # aa= queryset.filter(name=queryset[0]).values('script_path')

    def save_model(self, request, obj, form, change):
        """
        重写保存方法
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        current_path = ""
        obj.creater = request.user.last_name+request.user.first_name
        # print(dir(request.user))
        upload_to_path = "%s/%s/%s/" % (get_upload_path(), obj.project_name, obj.class_name)
        pre_data_path = "%s/%s/%s/" % (get_pre_data_path(), obj.project_name, obj.class_name)
        # 如果是编辑／修改
        if change:
            obj_original = self.model.objects.get(pk=obj.pk) # 获得修改前的对象
            obj_original_script = str(obj_original.script_path)
            obj_original_pre = str(obj_original.pre_data_file)
            # 修改的时候如果选择了新的脚本路径
            if str(obj.script_path).find('/') == -1:
                obj_script = upload_to_path + str(obj.script_path)
                original_path = get_files_path_common(obj_original_script, config_path=MEDIA_ROOT)
                current_path = get_files_path_common(obj_script, config_path=MEDIA_ROOT)
                # print current_path,original_path
                if str(obj.script_path) != "":
                    remove_file_common(current_path)
                if original_path.find('.') > -1:
                    remove_file_common(original_path)
            if str(obj.pre_data_file).find('/') == -1:
                # print obj.pre_data_file
                obj_pre = pre_data_path + str(obj.pre_data_file)
                original_pre_path = get_files_path_common(obj_original_pre, config_path=MEDIA_ROOT)
                current_pre_path = get_files_path_common(obj_pre, config_path=MEDIA_ROOT)
                # print current_pre_path,original_pre_path
                if str(obj.pre_data_file) != "":
                    remove_file_common(current_pre_path)
                if original_pre_path.find('.') > -1:
                    remove_file_common(original_pre_path)
                # write_path = current_path
            # # 修改的时候没有选择新的脚本路径，如：只是改了名字
            # else:
            #     write_path = Data.get_file_path(obj_original_script, config_path=MEDIA_ROOT)
        else:
            obj_script = upload_to_path + str(obj.script_path)
            obj_pre = pre_data_path + str(obj.pre_data_file)
            current_path = get_files_path_common(obj_script, config_path=MEDIA_ROOT)
            current_pre_path = get_files_path_common(obj_pre, config_path=MEDIA_ROOT)
            # print current_path
            if current_path.find('.') > -1:
                remove_file_common(current_path)

            if current_pre_path.find('.') > -1:
                remove_file_common(current_pre_path)
            # write_path = current_path
        ApiTest._meta.get_field("script_path").upload_to = upload_to_path
        ApiTest._meta.get_field("pre_data_file").upload_to = pre_data_path
        # Data.write_config("WishDeal", obj_original_name, (obj.name).encode("utf-8"), write_path, change)
        obj.save()
    make_story_public.short_description = "执行测试"
    clear_action.short_description = "数据初始化"


@admin.register(ProjectConfig)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    def save_model(self, request, obj, form, change):
        project_name = obj.name
        project_type = 'api'
        oraginal_name = ''
        if change:
            obj_original = self.model.objects.get(pk=obj.pk)
            oraginal_name = obj_original.name
        # update_total_project(project_type, project_name, change, oraginal_name)
        obj.save()
        t1 = threading.Thread(target=update_total_project, args=(project_type, project_name, change, oraginal_name))
        t1.setDaemon(True)
        t1.start()


@admin.register(VersionConfig)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('project','name')
    list_filter = ('project__name',)
    search_fields = ('project__name',)
