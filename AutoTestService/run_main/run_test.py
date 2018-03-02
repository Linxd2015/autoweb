#encoding:utf-8
"""
对web端暴露的接口
"""
import os,json
import threading
import sys
from AutoTestService import configSetting
from AutoTestService.utility import Data
from AutoTestService.base import LogController


def run_test(queryset,group,app_info):
    """
    执行测试的线程
    :param queryset:
    :return:
    """
    t1 = threading.Thread(target=run_case, args=(queryset,group,app_info))
    t1.setDaemon(True)
    t1.start()


def clear_run_actions(queryset,app_info):
    """
    初始化执行
    :param queryset:
    :return:
    """
    Data.clear_run_test(app_info)
    Data.write_chart_db(is_clear=True)


def clear_chart_info():
    Data.write_chart_db(is_clear=True)


def run_case(queryset, group, app_info=None):
    """
    执行测试case
    :param queryset:
    :return:
    """
    config_info = {}
    run_id = []
    for e in queryset:
        # print "开始执行"
        class_name = str(e.class_name)
        function_name = str(e.name)
        project_name = str(e.project_name)
        case_path = str(e.script_path)
        run_id.append(int(e.id))
        function_dic = {}
        function_dic[function_name] = case_path
        if not config_info.has_key(project_name):
            function_info = []
            class_info = {}
            function_info.append(function_dic)
            class_info[class_name] = function_info
            config_info[project_name] = class_info
        elif not config_info.get(project_name).has_key(class_name):
            function_info = []
            class_info = {}
            function_info.append(function_dic)
            config_info.get(project_name)[class_name] = function_info
        else:
            function_info = config_info.get(project_name).get(class_name)
            function_info.append(function_dic)
            config_info.get(project_name)[class_name] = function_info
    config_info['run_id'] = {'run_id':run_id}
    Data.write_config(config_info, group, app_info)
    #     "获取case逻辑"
    #     for i in range(len(cases)):
    #         # print "类名" + class_name
    #         c = Activator.createTestObjectOrInstance(class_name)
    #         # print "实例化"
    #         # print cases[i]
    #         suite.addTest(c(cases[i]))
    # suite = unittest.TestSuite()
    # suite.addTest(unittest.makeSuite(TestService.TestService))
    log_name = "log.txt"
    with open(log_name, 'w+')as f:
        if group.lower() == "service":
            output = os.popen("python -m unittest AutoTestService.TestManage.WebTest.TestService")
        else:output = os.popen("python -m unittest AutoTestService.TestManage.WebTest.TestApi")
        f.write(output.read())


def start_interface_test(run_list):
    if 'service' in run_list and 'api' in run_list:
        LogController.write_log("111111" + '\n')
        os.popen("python -m unittest AutoTestService.TestManage.WebTest.PlanServiceTask")
        LogController.write_log("2222" + '\n')
        os.popen("python -m unittest AutoTestService.TestManage.WebTest.PlanApiTask")
    elif 'service'in run_list:
        os.popen("python -m unittest AutoTestService.TestManage.WebTest.PlanServiceTask")
    elif 'api' in run_list:
        os.popen("python -m unittest AutoTestService.TestManage.WebTest.PlanApiTask")


def get_files_path_common(filename, config_path=None, **kwargs):
    """
    获取文件path
    :param filename:
    :param config_path:
    :param kwargs:
    :return:
    """
    return Data.get_file_path(filename, config_path)


def remove_file_common(file_name, path=None, **kwargs):
    """
    删除文件
    :param file_name:
    :param path:
    :param kwargs:
    :return:
    """
    return Data.remove_file(file_name,path)


def get_upload_path():
    """
    获取上传目录
    :return:
    """
    return configSetting.UPLOAD_PATH


def get_pre_data_path():
    """
    获取前置数据文件的目录
    :return:
    """
    return configSetting.PRE_DATA_PATH


def get_db_info(project_type,query_info):
    if project_type == "service":
        sql = "select * from service_autotest where name = '%s'" % query_info
    else:sql = "select * from api_apitest where name = '%s'" % query_info
    return Data.get_db_info(sql)


def write_run_task(task_name,original_name):
    Data.write_run_task_v2(task_name,original_name)


def start_task(task_name,run_info,is_run=True,project_name=""):
    if run_info.get('run_time')=='星期一':
        run_info['run_time']=0
    elif run_info.get('run_time')=='星期二':
         run_info['run_time']=1
    elif run_info.get('run_time')=='星期三':
         run_info['run_time']=2
    elif run_info.get('run_time')=='星期四':
         run_info['run_time']=3
    elif run_info.get('run_time')=='星期五':
         run_info['run_time']=4
    elif run_info.get('run_time')=='星期六':
         run_info['run_time']=5
    elif run_info.get('run_time')=='星期日':
         run_info['run_time']=6
    write_status = Data.write_run_task_v2(task_name,is_run=is_run)
    # write_status = {'code':1,'data':['UserInfo','PromoCard']}
    if write_status.get('code'):
        Data.PlanTask(task_name)
        project_list = write_status.get('data')
        temp = ''
        for i in range(len(project_list)):
            if i == 0:
                temp += '('
            if i == len(project_list) - 1:
                temp += '\'%s\'' % project_list[i] + ')'
            else:temp += '\'%s\''% project_list[i] +','
        sql = 'select DISTINCT(project_type) from timetask_totalprojects where project_name in %s' % temp
        LogController.write_log(sql)
        result = Data.get_sqlite_info(sql)
        run_list = []
        for item in result:
            run_list.append(item[0])
        Data.start_plan_task(start_interface_test,task_name, run_info,run_list)


def stop_task(task_name):
    Data.del_task(task_name)
    stop_status = Data.stop_plan(task_name)
    if not stop_status:
        Data.del_db_info("", configSetting.PLAN_JOB_TABLE, "where id = '%s'" % task_name)


def del_task(task_id,task_name):
    Data.stop_plan(task_name)
    Data.del_task(task_name,True)
    Data.del_db_info("","timetask_plantastconfig","where id = %d" % task_id)
    Data.del_db_info("","timetask_plantastconfig_plan_info","where plantastconfig_id = %d" % task_id)


def get_sqlite_info(name):
    sql = "select * from %s where id ='%s'" % (configSetting.PLAN_JOB_TABLE,name)
    act_task_list = Data.get_sqlite_info(sql)
    return act_task_list


def get_task_status(task_name):
    return Data.get_plan_task_status(task_name)


def get_chart():
    return Data.get_chart_info()


def update_total_project(project_type,project_name,change,original=""):
    if change:
        sql = 'update timetask_totalprojects set project_type =\'%s\',project_name =\'%s\' WHERE ' \
              'project_name = \'%s\'' % (project_type,project_name,original)
    else:
        sql = 'insert into timetask_totalprojects (project_type,project_name) VALUES (\'%s\',\'%s\')' % (project_type,project_name)
    # return sql
    Data.update_db_data(sql)
    return 1

def job():
    print "job1"

if __name__ == '__main__':
    # print get_sqlite_info('1111')
    # stop_task('service','UserInfo')
    # sql = "update timetask_totalprojects set project_type ='api',project_name ='dddfff' WHERE project_name = 'ddd'"
    # Data.update_db_data(sql)
    start_task("dd",{'run_type':'间隔固定分钟','run_time':'1'})
    # log_name = "log.txt"
    # with open(log_name, 'w+')as f:
    #     output = os.popen("python -m unittest AutoTestService.TestManage.WebTest.TestService")
    #     f.write(output.read())