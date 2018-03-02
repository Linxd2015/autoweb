#encoding:utf-8
import json
import sys
import traceback
import xlrd
import xlwt
import yaml
from AutoTestService import configSetting
from AutoTestService.base import FileController
from AutoTestService.base import Common
from AutoTestService.base.DBController import DBController
from AutoTestService.base.ApiController import *
from AutoTestService.base.RedisController import RedisController
from AutoTestService.base import LogController
from AutoTestService.configSetting import *
from AutoTestService.config.chartReport import *
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import time
import logging
reload(sys);
sys.setdefaultencoding("utf8")

PLAN_TIME = ""
PLAN_TASKS={}
class script(object):
    """
    暂时无用
    """
    def __get__(self, obj, type=None):
           pass
    def __set__(self, obj, val):
        pass
    def __delete__(self, obj):
        pass


class Descriptor(object):
    '''
    使用描述符来实现接口数据的传递，避免在跑case的时候找不到脚本路径，只要在跑之前将脚本路径传递过来并且赋值给Descriptor
    的SCRIPT_FILE属性，那么SCRIPT_FILE属性就会存在Descriptor的__dic__中，然后在测试类中可以直接调用Descriptor.SCRIPT_FILE
    来找到脚本路径
    '''
    SCRIPT_FILE = script()


class Activator:
    '''本类用来动态创建类的实例'''
    @staticmethod
    def createTestObjectOrInstance(class_name,is_class=True, *args, **kwargs):
        '''动态创建类的实例。
        [Parameter]
        class_name - 类的全名（包括模块名）111
        *args - 类构造器所需要的参数(list)
        *kwargs - 类构造器所需要的参数(dict)
        [Return]
        动态创建的类的实例
        [Example]
        class_name = 'knightmade.logging.Logger'
        logger = Activator.createInstance(class_name, 'logname')
        '''
        # (module_name, class_name) = class_name.rsplit('.', 1)
        module_meta = __import__("AutoTestService.src.TestRunController.TestService", globals(), locals(), ["Test"+class_name])
        # module_meta = __import__("AutoTestService.src.TestGroups.Services.UserInfo.TestWishDeal", globals(), locals(), ["TestWishDeal"])
        class_meta = getattr(module_meta, "Test"+class_name)
        object = class_meta(*args, **kwargs)
        if is_class:
            return class_meta
        else:
            return object


def create_test_data(db_info, db_name, table_name, file_path,
                     create_sheet_name=None, delete_sheet_name=None, **kwargs):
    """
    创建测试数据
    :param db_info:
    :param db_name:
    :param table_name:
    :param file_path:
    :param create_sheet_name:
    :param delete_sheet_name:
    :param kwargs:
    :return:
    """
    # project_path = Common.get_project_path()  # 获取当前项目地址
    path = os.path.abspath(os.path.join(MEDIA_ROOT, file_path))  # 组装能够识别的文件path
    db = DBController()
    db.connect_mysql(db_info, db_name)
    try:
        if delete_sheet_name:
            del_list = delete_sql(table_name, path, create_sheet_name, delete_sheet_name)
            # 先进行数据清理操作
            for del_sql in del_list:
                db.exe_update(del_sql)
        if create_sheet_name:
            create_list = create_sql(table_name, path, create_sheet_name)
            # # 然后进行数据插入
            for insert_sql in create_list:
                # print insert_sql
                db.exe_update(insert_sql)
        db.connect_close()
        # print "前置操作执行成功"
    except Exception,e:
        db.connect_close()
        LogController.write_log("create_test_data处理失败，原因为：%s" % traceback.format_exc())
        raise e


class PlanTask:
    def __init__(self,name):
        jobstores = {
            # 'mongo': MongoDBJobStore(),
            'default': SQLAlchemyJobStore(url='sqlite:///%s' % join_path(BASE_DIR, 'db.sqlite3'))
        }
        executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(5)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 6
        }

        my_task = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
        # schedmy1.start()
        # print my_task
        PLAN_TASKS[name] = my_task


def delete_sql(table_name, file_path, create_sheet_name, delete_sheet_name, **kwargs):
    """
    组装批量删除语句
    :param table_name:
    :param file_path:
    :param create_sheet_name:
    :param delete_sheet_name:
    :param kwargs:
    :return:
    """
    print "省略"


def create_sql(table_name, file_path, create_sheet_name, **kwargs):
    """
    组装批量insert into 语句
    :param table_name:
    :param file_path:
    :param create_sheet_name:
    :param kwargs:
    :return:
    """
    print "省略"


def get_keys(data, sheet_name=None, **kwargs):
    """
    获取excel文件中sheet的标题行的有效的字段集合（如果是为空的列名不算有效的）
    :param data:
    :param sheet_name:
    :param kwargs:
    :return:
    """
    # data = xlrd.open_workbook(file_path)
    if sheet_name is not None:
        insert_table = data.sheet_by_name(sheet_name)
    else:insert_table = data
    insert_ncols_number = insert_table.ncols
    keys = []
    for i in range(insert_ncols_number):
        if insert_table.cell_value(0, i) == "null" or insert_table.cell_value(0, i) == "":
            break
        keys.append(insert_table.cell_value(0, i))
    return keys


def get_run_config(class_name):
    """
    获取运行配置runConfig
    :param class_name:
    :return:
    """
    path = Common.get_file_path("config/runyaml.yaml")
    f = open(path)
    run_config = yaml.load(f)
    return run_config.get(class_name)


def join_path(path,file):
    """
    组装路径
    :param path:
    :param file:
    :return:
    """
    return os.path.abspath(os.path.join(path,file))


def get_run_path(data, class_name):
    """
    根据调用的函数名称，来获取测试的配置的数据
    :param data:
    :param class_name:
    :return:
    """
    print "省略"


def init_test(run_config, sheet="Sheet1"):
    """
    根据调用的函数名称，来获取测试的配置的数据
    :param run_config:
    :param sheet:
    :return:
    """
    print "省略"


def get_response(project, class_name, function,params):
    """
    调用服务端的接口，得到返回值
    :param project:
    :param class_name:
    :param function:
    :param params:
    :return:
    """
    print "省略"


def api_response(request_type,url,params=None,cookie=None):
    """
    调用api的请求接口
    :param url:
    :param request_type:
    :param params:
    :param cookie:
    :return:
    """
    if request_type.lower() == "post":
        return http_post(url,params,cookie)
    else:
        return http_get(url,params,cookie)

# def get_media_file(classname,function):
#     """
#     获取接口数据文件的绝对路径
#     :param classname:
#     :param function:
#     :return:
#     """
#     try:
#         config = get_config()
#         file = config.get(classname, function)
#         script_file = join_path(BASE_DIR + MEDIA_URL, file)
#         return script_file
#     except Exception,e:
#         print e.message + "配置文件中方法路径未找到"


def get_file_path(filename,config_path=None,**kwargs):
    """
    获取项目文件的绝对路径
    :param filename:
    :param config_path:
    :param kwargs:
    :return:
    """
    print "省略"


def get_case_name(project_name,class_name,function):
    """
    获取case名称，暂时没有用
    :param project_name:
    :param class_name:
    :param function:
    :return:
    """
    print "省略"



def write_config(config_info, group, app_info):
    """
    根据执行的内容将需要执行的接口写入配置
    :param config_info:
    :return:
    """
    print "省略"


def get_class(class_name):
    m = __import__('AutoTestService.config.caseFileConfig', globals(), locals(), "Test"+class_name)
    c = getattr(m, "Test"+class_name)
    return c


def remove_file(file_name, path=None, **kwargs):
    """
    删除文件
    :param file_name:
    :param path:
    :param kwargs:
    :return:
    """
    FileController.remove_file(file_name,path)


def get_case_datas(pro,name,func,case_path):
    """
    从文件中获取用例的数据，并且根据接口返回不同的入参数据
    :param pro:
    :param name:
    :param func:
    :return:
    """
    print "省略"


def get_total_data(group,is_task=False):
    """
    从执行配置中读取需要执行的接口信息
    :return:
    """
    print "省略"


def get_total_data_v2(group,is_task=False):
    """
    从执行配置中读取需要执行的接口信息
    :return:
    """
    print "省略"



def pre_options(pre):
    """
    初始化前置条件的数据1、数据插入2、数据修改3、数据删除
    :param pre:
    :return:
    """
    print "省略"


def after_options(after):
    """
    初始化前置条件的数据 1、数据插入2、数据修改3、数据删除
    :param after: 数据
    :return: 执行的结果
    """
    print "省略"


def write_excel(results, run_ids=[], group=""):
    """
    将执行结果写入excel文件
    :param results:
    :return:
    """
    print "省略"


def get_app_info(group):
    """
    根据执行的app类型，找到相应的app_name model_name
    :param group:
    :return:
    """
    file_path = RUN_TEST_CONFIG.get(group.lower())
    config_info = FileController.get_config(file_path)
    app_name = config_info.get("app_info","app_name")
    model_name = config_info.get("app_info", "model_name")
    return {"app_name": app_name, "model_name": model_name}


def get_log_time(type):
    """
    根据日期类型获取当前的记录时间：date为日期格式，number为时间戳
    :return:
    """
    if DATA_FORMAT.lower() == 'date':
        timeArray = time.localtime()
        if type == "day":
            return time.strftime("%Y%m%d", timeArray)
        elif type == "hours":
            return time.strftime("%Y%m%d%H", timeArray)
        elif type == "minute":
            return time.strftime("%Y%m%d%H%M", timeArray)
        elif type == "second":
            return time.strftime("%Y%m%d%H%M", timeArray)
    elif DATA_FORMAT.lower() == 'number':
        return time.time()


def update_result(app_name, model_name, run_ids, result_path):
    """
    更新执行结果至数据库
    :param app_name:
    :param model_name:
    :param run_ids:
    :param result_path:
    :return:
    """
    print "省略"


def clear_run_test(table):
    """
    初始化测试用例
    :return:
    """
    print "省略"


def write_chart_info(project,is_success):
    print "省略"


def write_chart_db(project='', class_name='', function_name='',chart_type='', is_success=True, is_clear=False, **kwargs):
    """
    将执行结果依次写入到数据库中，后期会改成用redis存储
    :param project:
    :param is_success:
    :param is_clear:
    :param kwargs:
    :return:
    """
    try:
        # conn = sqlite3.connect(join_path(BASE_DIR, 'db.sqlite3'))
        db = DBController()
        db.connect_sqlite(join_path(BASE_DIR, 'db.sqlite3'))
        # c = conn.cursor()
        if is_clear:
            sql = "delete from  chart_chartconfig"
            db.exe_update(sql)
            # c.execute(sql)
        else:
            result = db.exe_query("SELECT id, name,success,failed  from chart_chartconfig where name = '%s' and "
                               "class_name ='%s' and function_name = '%s' and chart_type='%s'" %
                               (project,class_name,function_name,chart_type))
            if len(result)>0:
                for row in result:
                    success = row[2]
                    failed = row[3]
                    # print success,failed
                    if is_success:
                        if success > 0:
                            success += 1
                        else:success = 1
                    else:
                        if failed > 0:
                            failed += 1
                        else:failed = 1
                    db.exe_update("update chart_chartconfig set success=%d,failed=%d where name = '%s' and "
                               "class_name ='%s' and function_name = '%s' and chart_type='%s'" %
                              (success,failed,project,class_name,function_name,chart_type))
            else:
                if is_success:
                    db.exe_update("insert into chart_chartconfig(name,success,failed,class_name,function_name,chart_type) "
                        "VALUES ('%s',%d,%d,'%s','%s','%s')" % (project,1,0,class_name,function_name,chart_type))
                else:
                    db.exe_update(
                        "insert into chart_chartconfig(name,success,failed,class_name,function_name,chart_type) "
                        "VALUES ('%s',%d,%d,'%s','%s','%s')" % (project, 0, 1,class_name,function_name,chart_type))
        db.connect_close()
    except Exception,e:
        LogController.write_log("执行结果写入图表失败,because："+str(e.message))


def get_sqlite_info(sql):
    try:
        db = DBController()
        db.connect_sqlite(join_path(BASE_DIR, 'db.sqlite3'))
        result = db.exe_query(sql)
        db.connect_close()
        return result
    except Exception,e:
        db.connect_close()
        LogController.write_log(exe_result=traceback.format_exc(),sql=sql)


def get_db_info(sql,db_info=None):
    if DB_TYPE.lower() == "sqlite":
        result = get_sqlite_info(sql)
    else:
        result = ''
    return result


def stop_plan(task_name):
    if PLAN_TASKS.has_key(task_name):
        schedmy = PLAN_TASKS.get(task_name)
        schedmy.remove_job(task_name)
        PLAN_TASKS.pop(task_name)
        return 1
    else:
        return 0


def get_plan_task_status(task_name):
    if not PLAN_TASKS.has_key(task_name):
        return -1
    else:
        schedmy = PLAN_TASKS.get(task_name)
        return schedmy.state


def start_plan_task(function_name,task_name,run_info,run_list):
    try:
        sched_my=PLAN_TASKS.get(task_name)
        run_type = run_info.get('run_type')
        run_time = run_info.get('run_time')
        if run_type == '每周执行一次':
        # schedmy = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
            sched_my.add_job(function_name,
                            trigger='cron',
                            day_of_week=run_time,
                            hour=8, minute=00,
                            id=task_name,
                            replace_existing=True,
                            args=[run_list])
        elif run_type == '间隔固定小时':
            sched_my.add_job(function_name,
                            trigger='interval',
                            hours=int(run_time),
                            id=task_name,
                            replace_existing=True,
                            args=[run_list])
        elif run_type == '间隔固定分钟':
            sched_my.add_job(function_name,
                            trigger='interval',
                            minutes=int(run_time),
                            id=task_name,
                            replace_existing=True,
                            args=[run_list])
        else:LogController.write_log('没有配置执行方式，或者执行方式配置的不对')
        sched_my.start()
        # print schedmy.state
    except(KeyboardInterrupt, SystemExit):
        sched_my.remove_job(task_name)
        sched_my.remove_job(task_name)
        LogController.write_log('start_plan_task失败，原因是：%s' % traceback.format_exc())


def del_db_info(db_info,table,where):
    try:
        db = DBController()
        sql = "delete from %s %s" % (table,where)
        if DB_TYPE == 'sqlite' or DB_TYPE == 'sqlite3':
            db.connect_sqlite(join_path(BASE_DIR, 'db.sqlite3'))
        db.exe_update(sql)
        db.connect_close()
    except Exception,e:
        db.connect_close()
        LogController.write_log('del_db_info失败,原因是%s' % traceback.format_exc(),table=table,where=where)


def write_run_task(group,task_name,original_name=None,is_run=False,**kwargs):
    print "省略"


def write_run_task_v2(task_name,original_name=None,is_run=False,**kwargs):
    print "省略"


def del_task(task_name,del_run=False):
    print "省略"

def update_db_data(sql):
    try:
        db = DBController()
        db.connect_sqlite(join_path(BASE_DIR, 'db.sqlite3'))
        db.exe_update(sql)
        db.connect_close()
    except Exception,e:
        db.connect_close()
        LogController.write_log('update_db_data失败，原因是：%s' % traceback.format_exc())



if __name__ == "__main__":
    # write_chart_info('Userinfo',False)
    # decode('unicode_escape')
    b ={'中国':2}
    print b.get('中国')
    # aa = '\u4e2d\u56fd,sssss'
    # print aa.decode('unicode_escape')
    # f = open('log.txt','w')
    # f.writelines(str(aa))
    # del_db_info('aa','aa','bb')
    # from AutoTestService.utility.Data.PlanTask import *
    # name = "ssss"
    # aaa = {name:"xxx"}
    # print aaa
    # write_run_task('service','UserInfo',is_run=True)
    # print get_total_data_v2("api",True)
    # bb = PlanTimeTask("Userinfo")
    # # vvv = PLAN_TASKS.get("Userinfo")
    # start_plan_task(test,"Userinfo",{'run_type':'间隔固定时间','run_time':'8'})
    # print vvv
    # # vvv.add_job(job, trigger='cron', second='*/5', id="Userinfo", replace_existing=True)
    # vvv.start()
    # time.sleep(111)
    # start_task("a","Userinfo")
    # aaa = PlanTask()PLAN_TASKS
    # print aaa.name
    # print PlanTask.name
    #
    # bbb = PlanTask()
    # print PlanTask.name
