# myProject
说明<br>
=
由于本人第一次写程序，功能比较简单，代码方面肯定有很多问题。发到github也是为了发现自己的不足，大家发现的啥问题，可以及时告诉我，我会努力改正，谢谢！<br>

2、项目简述<br>
=

本项目是类似于自动化的管理web项目，主要因为由于公司最近在弄自动化，为了快速投入应用，就结合django的admin模块（因为admin有现成的web，自己的前端水平实在是烂写不好，就用现成的），自己写了一个架子。主要是在django的admin基础上进行二次开发，来满足我们自动化的要求。<br>
该项目有3个功能：<br>
  1）service／api的接口自动化管理<br>
  2）执行结果图表展示<br>
  3）计划任务（持续集成）<br>

该项目只有1个架子，核心的功能代码没有写，服务端接口的需要根据公司的实际情况来编写，不过如果是api可用的（即get，post等请求）



3、部署该项目的的支持<br>
=
1、安装django：pip install Django<br>
2、安装定时插件APScheduler：pip install apscheduler<br>
3、安装计划任务需要的插件SQLAlchemy：pip install SQLAlchemy<br>
4、安装excel组件xlrd，xlwt<br>
5、安装mysql插件mysqlDB：<br>
6、安装yaml插件<br>


2、运行命令<br>
=
进入到项目根目录：python manage.py runserver<br>

访问admin首页：http://127.0.0.1:8000/admin/        账号：admin  密码：luoranbinadmin
