#encoding:utf-8
import os

# 与路径相关的配置
# 所有文件上传的相对路径
UPLOAD_PATH = 'uploads/script/'
# 前置条件的数据文件上传路径
PRE_DATA_PATH = 'uploads/pre_data/'
# 项目所在的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 测试执行结果文件存放的路径
RESULT_PATH = "result"
RESULT_ROOT= "%s/%s" % ('media',RESULT_PATH)
# 多媒体文件存放的根目录
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# 程序运行记录的日志目录
LOG_PATH = os.path.join(BASE_DIR, 'AutoTestService/result/')


"""
测试数据标题映射（即：excel标题对应的字段）
"""
# 项目
PROJECT_CONFIG = ['project','project_name',u'项目']
# 测试类／api的版本
CLASS_CONFIG = ['class_name','version','class','object',u'类']
# 请求类型映射（api才会出现）
REQUEST_TYPE_CONFIG = ['request_type','type']
# 前置操作
PRE_CONFIG = ['pre_option','pre_data',u'预置条件',u'前置条件']
# 请求url（api才会出现）
URL_CONFIG = ['url']
# cookie（api才会出现）
COOKIE_CONFIG = ['cookie']
# 后置处理
AFTER_CONFIG = ['after_option','after_data',u'后置条件',u'结束操作']
# 接口参数（注：json格式的数据）
VALUE_CONFIG = ['values','value','parameter','parameters',u'参数',u'入参']
# 检查数据
ASSERT_CONFIG = ['assert','assert_datas','assert_data',u'检查']
# 接口名称
FUNCTION_CONFIG = ['function','interface',u'接口',u'方法']
# 备注
REMARK_CONFIG = ['remark','remarks',u'备注']
# 结果
WRITER_RESULT = ['result','data']

"""
PRE_CONFIG前置数据操作内容中支持的字段映射
"""
# 数据库
DB_PARAM_CONFIG =['db','database']
# redis
REDIS_PARAM_CONFIG = ['redis']
# 数据库操作
OPTION_ADD = ['add','create']
OPTION_DEL = ['delete','del']
OPTION_SELECT = ['select','query']
OPTION_CHANGE = ['change','editor','edit']
# 数据来源（ACTION_TYPE_FILE 表示从文件中取，ACTION_TYPE_SQL表示sql语句）
ACTION_TYPE_FILE = ['file','db','database']
ACTION_TYPE_SQL = ['sql']
# redis
REDIS_PARAM_CONFIG = ['redis']
# 配置的redis信息
REDIS_INFO = ['redis_info']
# 配置的redis名称
REDIS_NAME = ['redis_name']

"""
ASSERT_CONFIG检查内容中支持的字段映射
"""
# 其他检查项
ASSERT_OTHER_KEY = ["lenth","value","data"]
# 其他检查项-长度检查
ASSERT_LENTH = ["lenth","size"]
# 其他检查项-某个值检查
ASSERT_DIC_VALUE = ["dic_value"]

"""
系统执行配置
"""
# 运行配置文件为yaml（可以是yaml 和ini）
RUN_FILE_TYPE = 'yaml'
# 运行级别
CASE_LOAD_TYPE = "CASE"
# 日志记录的时间控制
DATA_FORMAT = 'date'
# 日志记录的时间级别
RESULT_TYPE = "day"
# 数据库类型
DB_TYPE = 'sqlite'

# 与文件相关的配置
# 数据库解析配置文件相对路径
DB_CONTROLLER_CONFIG = "AutoTestService/config/DbConfig.ini"
# 接口项目解析配置文件相对路径
PROJECT_CONTROLLER_CONFIG = "AutoTestService/config/ProjectConfig.ini"
# redis解析配置文件相对路径
REDIS_CONTROLLER_CONFIG = "AutoTestService/config/RedisConfig.xml"
# SERVICE_TEST_CONFIG = {"config/ServiceRunFile.ini"}
# 接口测试的数据来源文件相对路径
RUN_TEST_CONFIG = {"service": "AutoTestService/run_main/run_file/ServiceRunFile.ini", "api": "AutoTestService/run_main/run_file/ApiRunFile.ini"}
# API_TEST_CONFIG = "config/ApiRunFile.ini"
PLAN_TASK_CONFIG = 'AutoTestService/run_main/run_file/PlanTaskFile.ini'
PLAN_JOB_TABLE = 'apscheduler_jobs'
