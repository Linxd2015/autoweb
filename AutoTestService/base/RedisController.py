# encoding: utf-8
import redis
from xml.dom.minidom import parse
import xml.dom.minidom
import os
import Common
from .. import configSetting


class RedisController:
    """
        redis操作的模块，封装了相关redis操作
        需要其他的方法，可自行扩展
    """
    redis_list = []

    def __init__(self, project_name=None, redis_name=None):
        if project_name is not None and redis_name is not None:
            self.get_redis(project_name, redis_name)

    def get_redis(self, project_name, redis_name):
        """
        链接redis，得到redis的实例
        :param project_name:
        :param redis_name:
        :return: list 由于redis 可能是集群，所以得到的是一个list，包含所有符合条件的redis 集合
        """
        project_path = Common.get_project_path()
        file_path = os.path.abspath(os.path.join(project_path, configSetting.REDIS_CONTROLLER_CONFIG))
        DOMTree = xml.dom.minidom.parse(file_path)
        root = DOMTree.documentElement
        redis_info = []
        # print root
        projects = root.getElementsByTagName("project")
        for project in projects:
            if project.hasAttribute("name"):
                if project.getAttribute("name") == project_name.lower():
                    items = project.getElementsByTagName("Resource")
                    for item in items:
                        # print item.getAttribute("redisName")
                        if item.getAttribute("redisName") == redis_name:
                            hosts = item.getElementsByTagName('host')
                            ports = item.getElementsByTagName('port')
                            dbs = item.getElementsByTagName('db')
                            host_tmp, port_tmp, db_tmp = hosts[0], ports[0], dbs[0]
                            host, port, db = host_tmp.firstChild.data, port_tmp.firstChild.data, db_tmp.firstChild.data
                            # print host, port, db
                            r = redis.StrictRedis(host=host, port=port, db=db)
                            redis_info.append(r)
        self.redis_list = redis_info
        return redis_info

    def get(self, key, list_redis=[],**kwargs):
        """
        get key的值
        :param key:
        :param list_redis:
        :param kwargs:
        :return:
        """
        value = ""
        if len(list_redis) > 0:
            _redis_list = list_redis
        else:_redis_list = self.redis_list
        for r in _redis_list:
            value=r.get(key)
        # print value
        return value

    def hgetall(self, key, list_redis=[],**kwargs):
        """
        hgetall key的值
        :param key:
        :param list_redis:
        :param kwargs:
        :return:
        """
        value = ""
        if len(list_redis) > 0:
            _redis_list = list_redis
        else:_redis_list = self.redis_list
        for r in _redis_list:
            value = r.hgetall(key)
        # print value
        return value

    def set(self, key,value,list_redis=[],**kwargs):
        """
        set key 的值
        :param key:
        :param value:
        :param list_redis:
        :param kwargs:
        :return:
        """
        if len(list_redis) > 0:
            _redis_list = list_redis
        else:_redis_list = self.redis_list
        try:
            result = _redis_list[0].set(key, value)
            # print value
            return result
        except redis.RedisError, msg:
            raise msg

    def delete(self,key,list_redis=[],**kwargs):
        if len(list_redis) > 0:
            _redis_list = list_redis
        else:_redis_list = self.redis_list
        try:
            for r in _redis_list:
                value = r.delete(key)
                return value
        except redis.RedisError, msg:
            raise msg

if __name__ == "__main__":
    re = RedisController("promocard", "promoCardData")
    re.get("new_user_coupon_2000042370")
    re.set("test1", "dddd")
