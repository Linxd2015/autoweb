# myProject
说明<br>
=
由于本人第一次写程序，功能比较简单，代码方面肯定有很多问题。发到github也是为了发现自己的不足，大家发现的啥问题，可以及时告诉我，我会努力改正，谢谢！<br>

2、项目简述<br>
=

本项目是类似于自动化的管理web项目，主要因为由于公司最近在弄自动化，为了快速投入应用，就结合django的admin模块（因为admin有现成的web，自己的前端水平实在是烂写不好，就用现成的），自己写了一个架子。主要是在django的admin基础上进行二次开发，来满足我们自动化的要求。<br>
该项目是数据驱动型框架，有3个功能：<br>
  1）service／api的接口自动化管理<br>
  2）执行结果图表展示<br>
  3）计划任务（持续集成）<br>

该项目只有1个架子，核心的功能代码没有写，服务端接口的需要根据公司的实际情况来编写，不过如果是api可用的（即get，post等请求）<br>

3、详细介绍<br>
=
该项目大致分为以下几大块<br>
-
1）接口逻辑服务层：AutoTestService（后续也可以独立出来）<br>
这里包含了，各种底层方法（base），运行配置（config），接口的底层逻辑（TestManage），公共方法（utility）<br>

2）各种app<br>
api、chart、service、timetask 都是django里面的app<br>

3）静态文件<br>
media文件下<br>

4）配置文件有2个：<br>
--》AutoTestService里面有一个configSetting.py：各种映射，接口执行配置<br>
--》autoweb里面又一个settings.py：django的配置<br>


其他说明<br>
-
1、web里面调用的AutoTestService的入口都在 AutoTestService／run_main里面（相当于是AutoTestService对外暴露的接口，方便以后有分离的需求）<br>

2、整体思路：主要利用的unittest + ddt。但是整合了所有接口的逻辑形成了一个统一调度接口，所以在代码只看到一个testRun方法（autoweb/AutoTestService/TestManage/WebTest/下的文件），这个方法将接口测试的逻辑统一进行了封装。数据获取->组装入参->预处理->接口调用->数据检查->数据清理->日志收集一>系列流程<br>

3、执行过程：<br>
将执行数据写入配置，等到真正执行的时候再从配置中读取执行数据，在执行数据中逐一获取需要执行的接口，然后通过ddt去获取相应接口的数据来调用统一调度接口来驱动测试<br>

3、好处：<br>
不用维护接口逻辑，只维护接口的数据。新增、修改接口的时候，不用再去手动增加test_xxx的接口方法，只需要增加相应的测试数据即可<br>


3、运行该项目的的支持<br>
=
1、安装django：pip install Django<br>
2、安装定时插件APScheduler：pip install apscheduler<br>
3、安装计划任务需要的插件SQLAlchemy：pip install SQLAlchemy<br>
4、安装excel组件xlrd，xlwt<br>
5、安装mysql插件mysqlDB：<br>
6、安装yaml插件<br>
7、安装ddt


2、运行命令<br>
=
进入到项目根目录：python manage.py runserver<br>

访问admin首页：http://127.0.0.1:8000/admin/        账号：admin  密码：luoranbinadmin
