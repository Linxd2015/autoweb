# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from service.admin import *
from django.shortcuts import redirect
from .forms import AddForm,CheckForm
import json
from models import Column,Article
import subprocess
from autoweb.settings import *
from AutoTestService.run_main.run_test import get_chart


def test_page(request):
    """
    测试数据构造页面
    :param request:
    :return:
    """
    if request.method == 'POST':
        str_result_tmp = request.POST['result']
        select_type = request.POST['select_type']
        form = AddForm(request.POST)
        if select_type.lower() == "database" or select_type.lower() == "db":
            result = {}
            print "POST逻辑"
            if form.is_valid():
                db_name = form.cleaned_data['db_name']
                table_name = form.cleaned_data['table_name']
                add_sheet = form.cleaned_data['add_sheet']
                del_sheet = form.cleaned_data['del_sheet']
                file_path = request.POST['file_path']
                # file_path = form.cleaned_data['file_path']
                # print form.cleaned_data['pre_data']
                type = request.POST['select_type']
                print file_path,type
                info = form.cleaned_data['info']
                dic_pre_data = {"db_info":info,
                                "db_name":db_name,
                                "table":table_name,
                                "create_sheet_name":add_sheet,
                                "delete_sheet_name":del_sheet,
                                "option":"add",
                                "data":file_path,
                                "type":"file"}
                if len(str_result_tmp) > 0:
                    # print 222222
                    # print str_result_tmp
                    result = json.loads(str_result_tmp)
                    if result.has_key("database"):
                        list_pre_data = result.get("database")
                        list_pre_data.append(dic_pre_data)
                        result["database"] = list_pre_data
                    else:result["database"] = [{"db_info":info,
                                                "db_name":db_name,
                                                "table":table_name,
                                                "create_sheet_name":add_sheet,
                                                "delete_sheet_name":del_sheet,
                                                "option":"add","data":file_path,
                                                "type":"file"}]
                else:
                    result["database"] = [{"db_info":info,
                                           "db_name":db_name,
                                           "table":table_name,
                                           "create_sheet_name":add_sheet,
                                           "delete_sheet_name":del_sheet,
                                           "option":"add",
                                           "data":file_path,
                                           "type":"file"}]
            print result
            return render(request, 'test.html', {'form': form, 'test': json.dumps(result)})
        elif select_type.lower() == "redis":
            result = {}
            if form.is_valid():
                redis_info = form.cleaned_data['redis_info']
                redis_name = form.cleaned_data['redis_name']
                redis_data = form.cleaned_data['redis_data']
                # redis_option = form.cleaned_data['redis_option']
                redis_option = request.POST['redis_option']
                redis_key = form.cleaned_data['redis_key']
                # print redis_name,redis_data
                dic_pre_data = {"redis_info": redis_info,
                                "redis_name": redis_name,
                                "option":redis_option,
                                "redis_key":redis_key,
                                "data": redis_data,}
                if len(str_result_tmp) > 0:
                    result = json.loads(str_result_tmp)
                    print result
                    if result.has_key("redis"):
                        list_pre_data = result.get("redis")
                        list_pre_data.append(dic_pre_data)
                        result["redis"] = list_pre_data
                    else:
                        result["redis"] =[{"redis_info": redis_info,
                                           "redis_name": redis_name,
                                           "option":redis_option,
                                           "redis_key": redis_key,
                                           "data": redis_data,}]
                else:
                    result["redis"] = [{"redis_info": redis_info,
                                        "redis_name": redis_name,
                                        "option":redis_option,
                                        "redis_key": redis_key,
                                        "data": redis_data,}]
            # print info ,type,result
            return render(request, 'test.html', {'form': form, 'test': json.dumps(result)})
        else:
            result = {}
            # return render(request, 'test.html', {'form': form,'test': "测试测试"})
            if form.is_valid():
                info = form.cleaned_data['info']
                db_name = form.cleaned_data['db_name']
                db_command= request.POST['db_command_str']
                dic_pre_data = {"db_info":info,"db_name":db_name,"data":db_command,"type":"sql"}
                if len(str_result_tmp) > 0:
                    result = json.loads(str_result_tmp)
                    print result
                    if result.has_key("database"):
                        list_pre_data = result.get("database")
                        list_pre_data.append(dic_pre_data)
                        result["database"] = list_pre_data
                    else:
                        result["database"] = [{"db_info":info,
                                               "db_name":db_name,
                                               "data":db_command,
                                               "type":"sql"}]
                else:
                    result["database"] = [{"db_info":info,
                                           "db_name":db_name,
                                           "data":db_command,
                                           "type":"sql"}]
            # print result
            return render(request, 'test.html', {'form': form, 'test': json.dumps(result)})
    else:
        form = AddForm()
    return render(request,'test.html',{'form': form,'test': ""})


def check_page(request):
    """
    测试辅助功能页面
    :param request:
    :return:
    """
    form = CheckForm(request.POST)
    log_str = ""
    if request.method == "POST":
        if form.is_valid():
            # check_value = request.POST['check_data']
            check_value = form.cleaned_data['check_data']
            select_type = form.cleaned_data['select_type']
            if select_type == "check_format":
                try:
                    json.loads(check_value)
                    log_str = "数据格式正确！"
                except Exception,e:
                    erro_log = e.message
                    log_str = "数据格式有误！，请检查，\n" \
                              "1）重点在于引号\"\",大括号{},中括号[]是否成对\n" \
                              "2）是否是正确的格式\n" \
                              "代码错误信息（调试用）："+ erro_log
            elif select_type == "array_json":
                print check_value
                code = """<?php
                    try{
                          echo json_encode(""" + check_value + """);
                          }
                    catch(Exception $e)
                        {echo "数据有问题！";}
                    ?>
                    """
                log_str = php_submit(code)
            elif select_type == "json_array":
                log_str = json_change_array(check_value)
            elif select_type == "sharding":
                code = """<?php
                            $arg = """+check_value+""";
                            $arg = substr($arg, -3);

                            $cfg = floor($arg % 128 / 8 / 4) + 1;

                            $db = floor($arg % 128 / 8);

                            $table = $arg % 128;

                            echo "服务器实例：{$cfg}\n";

                            echo "数据库：{$db}\n";

                            echo "表：{$table}\n";
                                ?>
                                """
                log_str = php_submit(code)
            return render(request, 'check.html', {'form':form,'test': log_str})
    else:
        return render(request,'check.html',{'form':form,'test': ""})


def add(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    return HttpResponse(str(a+b))




def php_submit(code):
    # open process
    p = subprocess.Popen(['php'], stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                         stderr=subprocess.STDOUT, close_fds=True)
    # read output
    o = p.communicate(code)[0]

    # kill process
    try:
        os.kill(p.pid, subprocess.signal.SIGTERM)
    except:
        pass
    # return
    return o


def json_change_array(value):
    data = value.replace(":","=>")
    data = data.replace("{", "array(")
    data = data.replace("}", ")")
    data = data.replace("\\", "")
    data = data.replace("[","array(")
    data = data.replace("]", ")")
    return data


def get_class(request, project_id):
    classs = ObjectConfig.objects.filter(project=project_id)
    print classs
    result = []
    for i in classs:
        result.append({'id':i.id,'name':i.name})
    return HttpResponse(json.dumps(result),content_type="application/json")




