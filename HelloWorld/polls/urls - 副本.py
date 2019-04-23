# -*- coding:utf-8 -*-

from django.urls import path
from . import views

app_name = 'polls' # for Django differentiate the URL names between apps

urlpatterns = [
    path('',views.index,name='index'),# ex: /polls/
    # the 'name' value as called by the {% url %} template tag
    path('<int:question_id>/',views.detail,name='detail'),# ex: /polls/5/
    path('<int:question_id>/results/',views.results,name='results'),# ex: /polls/5/results/
    path('<int:question_id>/vote/',views.vote,name='vote'),# ex: /polls/5/vote/
]
