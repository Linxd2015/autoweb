# encoding: utf-8
import ConfigParser
import os
import MySQLdb
import sqlite3
import Common
from AutoTestService import configSetting
from AutoTestService.base import LogController
import traceback


class DBController:
    status = None
    connect = None
    cursor = None
    _is_init = False

    def __init__(self, dbinfo=None, db=None):
        if dbinfo is not None and db is not None:
            conn_info = self.get_dbinfo(dbinfo)
            self.host = conn_info.get("host")
            self.user = conn_info.get("user")
            self.password = conn_info.get("password")
            self.db = db
            self.port = int(conn_info.get("port"))
            self._is_init = True

    def connect_mysql(self, dbinfo=None, database=None):
        """
        连接数据库
        :param dbinfo:
        :param database:
        :return:
        """
        try:
            # 如果数据库信息已经初始化，直接拿来用
            if self._is_init:
                connect = MySQLdb.connect(
                    host=self.host,
                    user=self.user,
                    passwd=self.password,
                    db=self.db,
                    port=self.port,
                    charset='utf8',
                )
                self.connect = connect
                self.cursor = connect.cursor(cursorclass=MySQLdb.cursors.DictCursor)  # 设置查询的结果变为字典型
                self.status = True
                return {"conn": connect, "cursor": connect.cursor()}
            # 如果数据库信息没有初始化，需要重新初始化信息
            else:
                conn_info=self.get_dbinfo(dbinfo)
                # print conn_info
                connect = MySQLdb.connect(
                    host=conn_info.get("host"),
                    user=conn_info.get("user"),
                    passwd=conn_info.get("password"),
                    db=database,
                    port=int(conn_info.get("port")),
                    charset='utf8',
                    )
                self.connect = connect
                self.cursor = connect.cursor(cursorclass=MySQLdb.cursors.DictCursor)  # 设置查询的结果变为字典型
                self.status = True
                return {"conn": connect, "cursor": connect.cursor()}
        except Exception,e:
            print "db connet is failed"
            raise e


    def connect_sqlite(self,db_file):
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()

    def connect_close(self):
        """
        关闭数据库链接
        :return:
        """
        try:
            self.cursor.close()
            self.connect.close()
            self.status = False
            self._is_init = False
        except:
            print "数据库连接关闭失败！"

    def get_dbinfo(self, info):
        """
        根据info读取配置获取数据库的配置信息
        :param info:
        :return:
        """
        config=ConfigParser.ConfigParser()
        project_path = Common.get_project_path()
        file_path = os.path.abspath(os.path.join(project_path, configSetting.DB_CONTROLLER_CONFIG))
        # print file_path
        config.readfp(open(file_path))
        db_info = {"host": config.get(info, "host"),
                   "port": config.get(info, "port"),
                   "user": config.get(info, "user"),
                   "password": config.get(info, "password")}
        return db_info

    def exe_query(self,sql):
        """
        执行查询时ql
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception, e:
            print "sql query is failed "
            raise e

    def exe_update(self, sql):
        """
        已知sql，执行更新语句
        :param sql:
        :return:
        """
        try:
            rows = self.cursor.execute(sql)
            self.connect.commit()
            return rows
        except Exception,e:
            self.connect.rollback()  # 发生错误时回滚
            self.cursor.close()
            self.connect.close()
            LogController.write_log("update_result处理失败。原因为:%s" % traceback.format_exc(),sql=sql)
            raise e

    def execute_insert(self, data, table):
        """
        执行插入语句：自己组装数据
        :param data:
        :param table:
        :return:
        """
        sql = "insert into %s VALUES (" % table
        try:
            for index in range(len(data)):
                if index != 0:
                    sql += ','+data[index]
                else:sql += data[index]
            sql += ')'
            # print sql
            rows = self.cursor.execute(sql)
            self.connect.commit()
            return rows
        except Exception, e:
            print "sql query is failed! "
            self.connect.rollback()
            raise e

    def execute_update(self, table=None, data=None, where=None,*args, **kwargs):
        """
        执行更新语句，自己组装数据
        :param table: 更新的表
        :param data: 更新的数据
        :param where: where条件
        :param args:
        :param kwargs:
        :return:
        """
        sql = "update %s set " % table
        try:
            keys = data.keys()
            for index in range(len(keys)):
                if index == 0:
                    if isinstance(data.get(keys[index]), int):
                        sql += "%s=%d" % (keys[index], data.get(keys[index]))
                    else:
                        sql += "%s='%s'" % (keys[index], data.get(keys[index]))
                else:
                    if isinstance(data.get(keys[index]), int):
                        sql += ",%s=%d" % (keys[index], data.get(keys[index]))
                    else:
                        sql += ",%s='%s'" % (keys[index], data.get(keys[index]))
            if where is not None:
                where_keys = where.keys()
                for index in range(len(where_keys)):
                    if index == 0:
                        if isinstance(where.get(where_keys[index]), int):
                            sql += " where %s=%d" % (where_keys[index], where.get(where_keys[index]))
                        else:
                            sql += " where %s='%s'" % (where_keys[index], where.get(where_keys[index]))
                    else:
                        if isinstance(where.get(where_keys[index]), int):
                            sql += " and %s=%d" % (where_keys[index], where.get(where_keys[index]))
                        else:
                            sql += " and %s='%s'" % (where_keys[index], where.get(where_keys[index]))
            # print sql
            rows = self.cursor.execute(sql)
            self.connect.commit()
            return rows
        except:
            self.connect.rollback()  # 发生错误时回滚

    def execute_delete(self, table=None, where=None,*args,**kwargs):
        """
        执行删除语句，带条件
        :param table: 删除的表
        :param where: where条件
        :param args:
        :param kwargs:
        :return:
        """
        sql = "delete from %s" % table
        try:
            if where is not None:
                where_keys = where.keys()
                for index in range(len(where_keys)):
                    if index == 0:
                        if isinstance(where.get(where_keys[index]), int):
                            sql += " where %s=%d" % (where_keys[index], where.get(where_keys[index]))
                        else:
                            sql += " where %s='%s'" % (where_keys[index], where.get(where_keys[index]))
                    else:
                        if isinstance(where.get(where_keys[index]), int):
                            sql += " and %s=%d" % (where_keys[index], where.get(where_keys[index]))
                        else:
                            sql += " and %s='%s'" % (where_keys[index], where.get(where_keys[index]))
            # print sql
        except:
            self.connect.rollback()  # 发生错误时回滚

    def execute_query(self, table=None, where=None,*args,**kwargs):
        """
        已知表，根据where来查询
        :param table:
        :param where:
        :param args:
        :param kwargs:
        :return:
        """
        sql = "delete from %s" % table
        try:
            if where is not None:
                where_keys = where.keys()
                for index in range(len(where_keys)):
                    if index == 0:
                        if isinstance(where.get(where_keys[index]), int):
                            sql += " where %s=%d" % (where_keys[index], where.get(where_keys[index]))
                        else:
                            sql += " where %s='%s'" % (where_keys[index], where.get(where_keys[index]))
                    else:
                        if isinstance(where.get(where_keys[index]), int):
                            sql += " and %s=%d" % (where_keys[index], where.get(where_keys[index]))
                        else:
                            sql += " and %s='%s'" % (where_keys[index], where.get(where_keys[index]))
            # print sql
        except Exception,e:
            print "sql query is failed "
            raise e






if __name__=='__main__':
    sql = "select * from tuanmei_user_wish_deals limit 1"
    db=DBController();
    db.connect_mysql("9001","tuanmei")
    #    # 执行SQL语句
    print db.exe_query(sql)
    # print cursor.execute(sql)
    # print cursor.fetchone()
    # print cursor.fetchone()
    # cursor.close()
    # db.close()
       # 提交修改
