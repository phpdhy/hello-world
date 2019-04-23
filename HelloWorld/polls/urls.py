# -*- coding:utf-8 -*-

from django.urls import path
from . import views
from django.views.generic import TemplateView,RedirectView

app_name = 'polls' # for Django differentiate the URL names between apps

urlpatterns = [
    
    path('aboutus/',TemplateView.as_view(template_name='polls/about.html'),name='aboutus'),# 直接用TemplateView,无需在views中定义class
    path('about/',views.AboutView.as_view(),name='about'),# 定义class方式使用TemplateView
    
    path('go-to-RedirectView/',RedirectView.as_view(url='https://docs.djangoproject.com/en/2.2/ref/class-based-views/base/#django.views.generic.base.RedirectView'),name='go-to-RedirectView'),
    
    path('',views.index,name='index'), # name不要忘了！！！
    path('index1/',views.IndexView1.as_view(),name='index1'),# ListView
    path('index2/',views.IndexView2.as_view(),name='index2'),# TemplateView
    
    #path('<slug:slug>/',views.DetailView.as_view(),name='detail'),
    path('<int:pk>/',views.DetailView.as_view(),name='detail'),          # DetailView
    path('<int:pk>/results/',views.ResultsView.as_view(),name='results'),# DetailView
    
    path('<int:question_id>/vote/',views.vote,name='vote'),# /polls/5/vote/
    
]
