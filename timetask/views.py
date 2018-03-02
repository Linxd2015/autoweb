# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from AutoTestService.run_main import run_test
from django.shortcuts import render
import time,json
from .models import PlanTimeConfig,PlanTastConfig
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def time_task_page(request):
    plan_info = PlanTastConfig.objects.all()
    result = []
    for item in plan_info:
        act_task_info = run_test.get_sqlite_info(item.name)
        status = run_test.get_task_status(str(item.name))
        result.append({'id': item.id,
                       'name': item.name,
                       'status':status,
                       'task_type':str(item.plan_type),
                       'plan_time':item.plan_time,
                       'run': 1 if len(act_task_info) > 0 else 0,
                       'next_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(act_task_info[0][1])) if len(act_task_info)>0 else ''})
    # for i in range(len(aa)):
    #     print aa[i][0],aa[i][1],aa[i][2]
    #     result.append({'id': aa[i][0], 'next_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(aa[i][1]))})
        # result.append({'id':aa[i][0],'next_time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(aa[i][1]))})
    # print aa
    return render(request,"admin/timetask/timetaskconfig/change_list.html",{'task':result})


def change_form(request):
    return render(request,'admin/timetask/timetaskconfig/change_list.html')


@login_required
def stop_task(request,task_id):
    plan_info = PlanTastConfig.objects.filter(id=task_id)
    task_name = plan_info[0].name
    # project_name =plan_info[0].project_name
    run_test.stop_task(task_name)
    # Data.stop_plan(task_name)
    # aa = plan.stop_plan()
    # return render(request, "timetask.html")
    return HttpResponseRedirect("/admin/timetask/plantastconfig/")
    # return render(request,"timetask.html")


@login_required
def del_task(request,task_id):
    plan_info = PlanTastConfig.objects.filter(id=task_id)
    task_name = plan_info[0].name
    # project_name = plan_info[0].project_name
    run_test.del_task(int(task_id),task_name)
    # Data.stop_plan(task_name)
    # Data.del_db_info("","","where id = %d"% int(task_id))
    # aa = plan.stop_plan()
    # return render(request, "timetask.html")
    return HttpResponseRedirect("/admin/timetask/plantastconfig/")
    # return render(request,"timetask.html")


@login_required
def start_task(request,task_id):
    # task_id = task_info.split('_')[1]
    plan_info = PlanTastConfig.objects.filter(id=task_id)
    task_name = plan_info[0].name
    # project_name = plan_info[0].project_name
    plan_type = plan_info[0].plan_type
    plan_time =plan_info[0].plan_time
    # print type(plan_type)
    # print type(u'豆豆豆')
    # print type(str(plan_type))
    run_info={'run_type':str(plan_type),'run_time':str(plan_time)}
    print run_info
    run_test.start_task(task_name,run_info,True)
    # Data.write_run_task(project_name,task_name,is_run=True)
    # Data.PlanTimeTask(task_name)
    # Data.start_plan_task(job,task_name)
    return HttpResponseRedirect("/admin/timetask/plantastconfig/")


@login_required
def get_plan_info(request, plan_id):
    plan_info = PlanTimeConfig.objects.filter(plan_type=plan_id)
    # print plan_info
    result = []
    for i in plan_info:
        result.append({'id':i.id,'name':i.name})
    return HttpResponse(json.dumps(result),content_type="application/json")

