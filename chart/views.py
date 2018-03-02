# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import ChartConfig
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from AutoTestService.run_main.run_test import get_db_info
from autoweb.settings import *
from django.contrib.auth.views import login_required
# Create your views here.
@staff_member_required
@login_required
def index(request):
    # home_display_columns = Column.objects.filter(home_display=True)
    # nav_display_columns = Column.objects.filter(nav_display=True)
    chart_info = []
    success_list = []
    failed_list = []
    success_dic = {}
    failed_dic = {}
    service_result_file = api_result_file = ""
    chart_items = ChartConfig.objects.all()
    i = j = 0
    for item in chart_items:
        print item
        chart_type = item.chart_type.encode("utf-8")
        project_name = item.name.encode("utf-8")
        if chart_type == "service" and i == 0:
            case_info = get_db_info("service",item.function_name.encode("utf-8"))
            print case_info
            if len(case_info)>0:
                service_result_file = MEDIA_URL + case_info[0][6]
                i += 1
        if chart_type == "api" and j == 0:
            case_info = get_db_info("api",item.function_name.encode("utf-8"))
            api_result_file = MEDIA_URL + case_info[0][6]
            j += 1
        if project_name not in chart_info:
            chart_info.append(project_name)
        if success_dic.has_key(project_name):
            success_number = success_dic.get(project_name)
            success_number += item.success
            success_dic[project_name] = success_number
        else:success_dic[project_name] = item.success
        if failed_dic.has_key(project_name):
            failed_number = failed_dic.get(project_name)
            failed_number += item.failed
            failed_dic[project_name] = failed_number
        else:failed_dic[project_name] = item.failed
    for chart_item in chart_info:
        success_list.append(success_dic.get(chart_item))
        failed_list.append(failed_dic.get(chart_item))
    options = {
        'xAxis': chart_info,
        'series_data': {
            'success': success_list,
            'failed': failed_list,
        }
    }
    print service_result_file,api_result_file
    # columns = Column.objects.all()
    return render(request, 'chart.html', {
        'option': options,
        'service_result_file':service_result_file,
        'api_result_file':api_result_file,
    })
    # return HttpResponse(u'欢迎来到测试首页')
