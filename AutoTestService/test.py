# encoding:utf-8
import threading
import os
import sched
import time
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import (EVENT_JOB_EXECUTED,EVENT_JOB_ERROR)
import sys
from urllib import quote_plus
from AutoTestService.utility.Data import *

# sched1 = BlockingScheduler(daemonic = False)
# url = 'mysql+mysqldb://root:luoranbin@localhost:3306/test'
# uri = "mongodb://%s:%s@%s" % (
#                 quote_plus(mongoDBuser), quote_plus(mongoDBpwd), '127.0.0.1:3306')
#
# # mongoclient = pymongo.MongoClient(uri)
# store = SQLAlchemyJobStore(url)
class my_sched:
    def __init__(self):
        self.mysched = BackgroundScheduler()
    def job(self):
        print "sssss"

    def run_test(self):
        os.system("python -m unittest AutoTestService.TestManage.WebTest.TestService")


    def print_file(self,log_file):
        for line in log_file:
            time.sleep(2)
            print line

    def add_my_job(self,functioin,id):
        self.mysched.add_job(functioin,trigger='cron',second = '*/5',id =id)

    def my_listener(self,event):
        if event.exception:
            print ('sfsdfsdfsdf')
        else:
            print "aaaaaaa"
    # def print_hello():
    #     print "Hello World"
    #     t = threading.Timer(3,print_hello)
    #     t.start()
    #
    # schedule = sched.scheduler(time.time,time.sleep)
    #
    # def execute_command(cmd, inc):
    #     os.system(cmd)
    #     schedule.enter(inc,0,execute_command,(cmd,inc))
    #
    # def main(cmd,inc=60):
    #     schedule.enter(0,0,execute_command,(cmd,inc))
    #     schedule.run()
    # def my_job():
    #     print "Hello World"
#
if __name__ == '__main__':
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
        'max_instances': 3
    }
    def job():
        print "第一个job"
    def job1():
        print "第二个job"
    # schedmy1 = my_sched()
    schedmy = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
    schedmy2 = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
    schedmy.add_job(job,trigger='cron',second = '*/5',id ='Userinfo',replace_existing=True)
    schedmy2.add_job(job1, trigger='cron', second='*/5', id='total')
    # url = sys.argv[1] if len(sys.argv)>1 else 'sqlite:///jobs.sqlite'
    # schedmy.add_jobstore('sqlalchemy',url=url)
    try:
        schedmy.start()
        schedmy2.start()
        print schedmy.state
        while True:
            # time.sleep(2)  # 其他任务是独立的线程执行
            # print('sleep!')
            bb = raw_input("aaaaa:")
            if bb == '1':
                # schedmy2.start()
                if schedmy.state == 0:
                    pass
                else:
                    schedmy.pause()
                print schedmy.state
                # schedmy.pause_job()
            elif bb == '2':
                if schedmy.state == 0:
                    schedmy.start()
                else:
                    schedmy.resume()
                print schedmy.state
                # schedmy.resume_job()
            elif bb == '3':
                # schedmy.remove_job('autotest')
                schedmy.shutdown()
                print schedmy.state


    except(KeyboardInterrupt,SystemExit):
        print 111
        # schedmy.remove_job('autotest')
        # schedmy.remove_job('autotest2')


    # schedmy.add_job(job,trigger='cron',second = '*/5',id ='autotest')
    # schedmy.add_listener(my_listener,EVENT_JOB_EXECUTED|EVENT_JOB_ERROR)
    # # aa = schedmy.get_jobs()
    # # print aa
    # schedmy.start()
    # try:
    #     with open('apscheduler_test.txt') as f:
    #         print_file(f)
    # except(KeyboardInterrupt,SystemExit):
    #     schedmy.remove_job('autotest')