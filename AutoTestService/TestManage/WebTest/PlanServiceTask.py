#encoding:utf-8
import unittest
from AutoTestService.utility.Data import *
from AutoTestService.base import LogController
import time
import ddt
import json

@ddt.ddt
class TestService(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.test_result = []
        self.test_run_id = []
        print "start testing"

    @classmethod
    def tearDownClass(self):
        write_excel(self.test_result, self.test_run_id, "service")
        # write_log("接口执行成功")
        print "end testing"

    @ddt.data(*get_total_data_v2("service",True))
    def test_Run(self,datas):
        """
        服务端接口测试统一调度方法
        :param datas:
        :return:
        """
        chart_type = 'service'
        # print datas
        if datas.has_key('run_id') and datas.get('run_id') is not None:
            for item in datas.get('run_id'):
                self.test_run_id.append(item)
        if not datas.has_key('request_title'):
            if datas.has_key('log_str'):
                log_str = datas.get('log_str')
            else:log_str = u'脚本里没有该接口的测试数据'
            self.test_result.append({'project': datas.get('project'),
                                     'class_name': datas.get('class_name'),
                                     'function': datas.get('function'),
                                     'parameter': u'未获取到',
                                     'result': {'code': False, 'response': log_str},
                                     'remark': "",
                                     'assert_data': "",
                                     'pre_data': "", 'after_data': ""})
            write_chart_db(datas.get('project'),datas.get('class_name'),datas.get('function'),chart_type,False)
        else:
            # 1、处理传入的数据，得到接口参数，与前置条件数据，后置处理数据，检查数据
            request_infos = datas.get('request_info')  # 接口主要处理数据：包含接口入参，检查数据，前置操作，后置操作
            request_title = datas.get('request_title')  # 请求头包含：项目名称，类，接口名称
            parameters = request_infos.get("parameters")  # 接口入参
            assert_data = request_infos.get("assert_datas")  # 检查数据
            pre_data = request_infos.get("pre_datas") if request_infos.has_key("pre_datas") else ""  # 前置条件数据
            # pre_data = ""
            after_data = request_infos.get("after_datas") if request_infos.has_key("after_datas") else ""  # 后置处理数据
            remark = request_infos.get("remark") if request_infos.has_key("remark") else ""
            # 2、进行预处理
            if pre_data:
                pre_options(pre_data)
            # 数据清理
            if after_data:
                after_options(after_data)
            # 3、组装接口入参
            params = []
            for item in parameters:
                params.append(item)
            # 4、调用接口得到返回值
            response = {}
            assert_key = ""
            try:
                response = get_response(request_title.get('project'), request_title.get('class'),
                                        request_title.get('function'), params)
            # 5、进行检查check
                for key in assert_data.keys():
                    # print "开始检查"
                    assert_key = key
                    if assert_key == "other":
                        other_assert_data = assert_data.get(key)
                        other_assert_key = other_assert_data.get("other_key")
                        value_list = other_assert_data.get("other_value")
                        for i in range(len(other_assert_key)):
                            other_key = other_assert_key[i]
                            if other_key in configSetting.ASSERT_OTHER_KEY:
                                if other_key in configSetting.ASSERT_LENTH:
                                    other_value_key = value_list[i].keys()
                                    assert_value = value_list[i].get(other_value_key[0])
                                    while isinstance(assert_value,dict):
                                        print "ssss"
                                    actual_value = len(response.get(other_value_key[i]))
                                    # print assert_value,actual_value
                                    self.assertTrue(assert_value == actual_value)
                                elif other_key in configSetting.ASSERT_DIC_VALUE:
                                    list_key = []
                                    other_value_key = value_list[i].keys()
                                    assert_value=value_list[i].get(other_value_key[0])
                                    list_key.append(other_value_key[0])
                                    while isinstance(assert_value,dict):
                                        key_tmp = assert_value.keys()[0]
                                        list_key.append(key_tmp)
                                        assert_value = assert_value.get(key_tmp)
                                    # print assert_value,list_key
                                    response_value = response
                                    actual_value = ""
                                    for i_key in list_key:
                                        response_value_tmp = response_value.get(i_key)
                                        if isinstance(response_value_tmp,dict):
                                            response_value = response_value_tmp
                                        else: actual_value = response_value_tmp
                                    self.assertTrue(actual_value == assert_value)
                    else:
                        self.assertTrue(assert_data.get(key) == response.get(key))
                log_str = u'成功'
                self.test_result.append({'project': request_title.get('project'),
                                         'class_name': request_title.get('class'),
                                         'function': request_title.get('function'),
                                         'parameter': json.dumps(parameters).decode("utf-8"),
                                         'result': {'code': True, 'response': log_str},
                                         'remark': remark, 'assert_data': assert_data,
                                         'pre_data': pre_data, 'after_data': after_data})
                write_chart_db(request_title.get('project'),request_title.get('class'),request_title.get('function'),chart_type, True)
            except Exception, e:
                if assert_data and assert_data is not None:
                    actual_response = response.get(assert_key) if response.has_key(assert_key) else (response if len(response) > 0 else e)
                    log_str = u"%s期望是%s,实际得到的是%s:"%(str(assert_key), str(assert_data.get(assert_key)), str(actual_response))
                else: log_str = u"检查结果数据有误或者缺失"
                self.test_result.append({'project': request_title.get('project'),
                                         'class_name': request_title.get('class'),
                                         'function': request_title.get('function'),
                                         'parameter': json.dumps(parameters).decode("utf-8"),
                                         'result': {'code': False, 'response': log_str},
                                         'remark': remark, 'assert_data': assert_data,
                                         'pre_data': pre_data, 'after_data': after_data})
                if not AssertionError:
                    LogController.write_log(traceback.format_exc())
                write_chart_db(request_title.get('project'),request_title.get('class'),request_title.get('function'),chart_type, False)
                # write_log("%s/%s/%s:失败了。原因为:%s" % (request_title.get('project'),request_title.get('class'),
                #                                    request_title.get('function'),log_str))
            # 6、记录日志

            # print response


if __name__=="__main__":
    # print TestWishDeal.__dict__
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestService)
    suite = unittest.TestSuite(suite1)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.TextTestRunner(verbosity=2).run(suite)

