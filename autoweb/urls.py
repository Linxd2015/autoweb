"""autoweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import *
from django.contrib import admin
from django.contrib.auth.views import login
from DjangoUeditor import urls
from django.conf import settings
from service.views import *
from api.views import *
from chart.views import *
from timetask import views

urlpatterns = [
    url(r'^admin/chart/chartconfig/', index, name='index'),
    url(r'^timetask/start_task/(?P<task_id>[0-9]+$)', views.start_task, name='start_task_page'),
    url(r'^admin/timetask/plantastconfig/$', views.time_task_page, name='time_task_page'),
    url(r'^timetask/stop_task/(?P<task_id>[0-9]+$)', views.stop_task, name='stop_task_page'),
    url(r'^timetask/del_task/(?P<task_id>[0-9]+$)', views.del_task, name='del_task_page'),
    url(r'^admin/', admin.site.urls),
    url(r'^ueditor/', include(urls)),
    url(r'^index/',index,name='index'),
    url(r'^test/',test_page,name='test'),
    url(r'^check',check_page,name='check'),
    url(r'^add/', add, name='add'),
    # url(r'^column/(?P<column_slug>[^/]+)/$', column_detail, name='column'),
    # url(r'^services/(?P<pk>\d+)/(?P<article_slug>[^/]+)/$', article_detail, name='article'),
    url(r'^service/get_class/(?P<project_id>[0-9]+)$',get_class),
    url(r'^timetask/get_plan_info/(?P<plan_id>[0-9]+)$',views.get_plan_info),
    url(r'^api/get_class/(?P<project_id>[0-9]+)$',get_api_class),
]
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)