# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import VersionConfig
from django.http import HttpResponse
from django.contrib.auth.views import login_required
import json

from django.shortcuts import render

# Create your views here.
@login_required
def get_api_class(request, project_id):
    classs = VersionConfig.objects.filter(project=project_id)
    print classs
    result = []
    for i in classs:
        result.append({'id':i.id,'name':i.name})
    return HttpResponse(json.dumps(result),content_type="application/json")