#encoding:utf-8
import ConfigParser
import sys
import traceback
import xlrd
import yaml
from AutoTestService.base import Common
from AutoTestService.base.ApiController import *
from AutoTestService.base import LogController
from AutoTestService.configSetting import *
reload(sys);
sys.setdefaultencoding("utf8")


class myconf(ConfigParser.ConfigParser):
    """
    重写ConfigParser类，解决section大小写的问题
    """
    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


def get_config(config_path):
    """
    获取配置文件的内容
    :return:
    """
    # print config_path
    filename = Common.get_path_by_relative_path(config_path)
    (shotname, extension) = filename.split('.')
    # aa=get_file_path(filename)
    if extension == "ini":
        config = myconf()
        config.readfp(open(filename,"r"))
    elif extension == "yaml":
        config = yaml.load(open(filename))
    return config


def write_config(config_info, group, app_info):
    """
    根据执行的内容将需要执行的接口写入配置
    :param config_info:
    :return:
    """
    try:
        writ_file = RUN_TEST_CONFIG.get(group.lower())
        config = get_config(writ_file)
        sections = config.sections()
        for sect in sections:
            config.remove_section(sect)
        for key in range(len(config_info.keys())):
            if config_info.keys()[key] == 'run_id':
                if not config.has_section('run_id'):
                    config.add_section('run_id')
                config.set('run_id','run_id',json.dumps(config_info.get('run_id').get('run_id')))
            else:
                project_name = config_info.keys()[key]
                class_info = config_info.get(project_name)
                for class_key in range(len(class_info.keys())):
                    class_name =class_info.keys()[class_key]
                    function_datas = class_info.get(class_name)
                    if not config.has_section(project_name):
                        config.add_section(project_name)
                    config.set(project_name,class_name,json.dumps(function_datas))
        for key in app_info.keys():
            if not config.has_section('app_info'):
                config.add_section('app_info')
            config.set('app_info',key,app_info.get(key))
        with open(Common.get_path_by_relative_path(writ_file), "w+") as f:
            config.write(f)
    except Exception,e:
        LogController.write_log("write_config处理失败，原因为：%s" % traceback.format_exc())


def remove_file(file_name, path=None, **kwargs):
    """
    删除文件
    :param file_name:
    :param path:
    :param kwargs:
    :return:
    """
    if path is not None:
        pass
    else:
        if os.path.exists(file_name):
            os.remove(file_name)


def get_excel_datas(file_path,sheet=None,**kwargs):
    """
    获取excel文件中的数据流
    :param file_path:
    :param sheet:
    :param kwargs:
    :return:
    """
    try:
        datas = xlrd.open_workbook(file_path)
        if sheet is not None:
            return datas.sheet_by_name(sheet)
        else:return datas
    except Exception,e:
        LogController.write_log("get_excel_datas处理失败，原因为：%s" % traceback.format_exc())


def writ_file(file_path,file_stream,file_dir=None):
    if file_dir is not None:
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
    file_stream.save(file_path)


