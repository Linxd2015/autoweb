#encoding:utf-8
from django import forms


class AddForm(forms.Form):
    # redis_choices = [('set','set'),('delete','del'),('get','get'),('hgetall','hgetall')]
    info = forms.CharField(label=u"数据库实例",required=False)
    db_name = forms.CharField(label=u"数据库名字",required=False)
    table_name = forms.CharField(label=u"数据库表名",required=False)
    add_sheet = forms.CharField(label=u"插入的sheet",required=False)
    del_sheet = forms.CharField(label=u"清除的sheet",required=False)
    redis_name = forms.CharField(label=u"缓存",required=False)
    redis_info = forms.CharField(label=u"项目", required=False)
    # redis_option = forms.ChoiceField(label=u"操作类型",required=False,choices=redis_choices)
    redis_key = forms.CharField(label=u"key", required=False)
    redis_data = forms.CharField(label=u"数据",required=False)
    file_path = check_data = forms.CharField(widget=forms.Textarea,required=False)


class CheckForm(forms.Form):
    check_data = forms.CharField(widget=forms.Textarea)
    select_type = forms.ChoiceField(choices=[('check_format', u'检查格式'), ('array_json', u'PHP array转json'),
                                             ('json_array', u'json转PHP array'), ('sharding', u'计算Sharding')])
    # file_path = forms.CharField(label=u"数据文件路径")
    # type = forms.ChoiceField(choices=[('database',u'数据库'),('redis',u'缓存')], label = u"数据类型")
    # pre_data = forms.CharField(label=u"数据", widget=forms.Textarea)
    # option = forms.ChoiceField(choices=[('add', u'插入'), ('del', u'删除'), ('update', u'更新')], label=u"操作类型")