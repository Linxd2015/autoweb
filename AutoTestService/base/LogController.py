#encoding:utf-8
from AutoTestService import configSetting
import os,time,sys


def write_log(log_str=None,exe_result=None,**kwargs):
    """
    记录日志
    :param log_str:
    :return:
    """
    print kwargs
    param_str = ''
    if len(kwargs)>0:
        for key in kwargs:
            param_str += '%s=%s ' % (key, kwargs[key])
    function_name = sys._getframe().f_back.f_code.co_name
    log_path = configSetting.BASE_DIR + '/AutoTestService/log'
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    f = open(configSetting.BASE_DIR + '/AutoTestService/log/%s.txt'
             % time.strftime('%Y%m%d', time.localtime(time.time())), 'a')
    if log_str is not None:
        f.writelines(time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time())) + str(log_str) + '\n')
    if param_str != '':
        log_reason = '%s 执行失败，参数为:%s' % (function_name,param_str)
        log_str = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time())) + log_reason +'\n'
        f.writelines(log_str)
    if exe_result is not None:
        f.writelines('原因为:%s' % exe_result)
    # f.writelines(time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time())) + str(log_str) + '\n')
    f.close()