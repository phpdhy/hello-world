# -*- coding:utf-8 -*-

from django.shortcuts import render,get_object_or_404
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from .models import Question,Choice
from django.db.models import F

# Create your views here.

'''
查看投票结果
'''
def results(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question':question})
    #return HttpResponse("The results of question %s" %question_id)

'''
投票并记录
'''
def vote(request,question_id):
    #return HttpResponse("Voting question %s" %question_id)
    question = get_object_or_404(Question,pk=question_id)
    try:
        # print('try 111')
        selected_choice = question.choice_set.get(pk=request.POST['choice']) 
        # selected_choice = question.choice_set.get(pk=request.POST.get('choice'))  # 效果同上，还可以提供默认值 .get('choice','1') 即：choice.id=1 
        # selected_choice = get_object_or_404(Choice,pk=request.POST.get('choice')) # 效果同上，直接get object可以
        # print('try 222')
    except KeyError:
        return render(request, 'polls/detail.html', {'question':question,'error_message':'您没有选择！'})
    except Choice.DoesNotExist:
        return render(request, 'polls/detail.html', {'question':question,'error_message':'您没有选择！！'})
    else:
        # selected_choice.votes += 1
        # Another useful benefit of F() is that having the database - rather than Python - update a field’s value avoids a race condition.
        # it will only ever update the field based on the value of the field in the database when the save() or update() is executed, rather than based on its value when the instance was retrieved.
        selected_choice.votes = F('votes') + 1 # Avoiding race conditions using F()，直接在DB层面修改数据，不读到内在中。详见：Python Query Expressions
        selected_choice.save()
        
        # F() objects assigned to model fields persist after saving the model instance and will be applied on each save(). For example:
        #selected_choice.choice_text = 'C语言'
        #selected_choice.save() # 不仅修改choice_text，还会把votes再加1
        
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,))) # Reverse function helps avoid having to hardcode a URL in the view function
        '''
                 注意！！！调试时总出错的原因是这里的   polls:results 错误地写成了 polls:vote，导致再次进入此方法而未提供question_id，出现Choice.DoesNotExist异常！
         Always return an HttpResponseRedirect after successfully dealing with POST data. This prevents data from being posted twice if a user hits the Back button.
                 在python中访问一个页面的几种方法：（代码中、页面中）
         1.return HttpResponse("The results of question %s" %question_id) ，                      直接response页面内容
         2.return render(request,'polls/results.html',{'question':question}) ，                直接render目标templates页面并传递context参数
         3.return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))，  按照urls中定义的path访问对应的view方法并传递path中定义的参数（有别于request参数）
         4.<a href="{% url 'polls:detail' question.id %}">，                           同3.
         5.<form action="{% url 'polls:vote' question.id %}" method="post">            同4.
        '''
        
'''
显示问题及选项
'''
def detail(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/detail.html',{'question':question})
    #return HttpResponse("Question %s" %question_id)

def index(request):
    #return HttpResponse("Hello,world.You're at the polls index.")
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #latest_question_list = Question.objects.filter(question_text__icontains='what').order_by('-pub_date')[:5] # 模糊查询，按时间倒序取前5
    context = {'latest_question_list':latest_question_list}
    return render(request,'polls/index.html',context)
    '''
        在粘贴以下中文内容前，必须先在此文件中第一行设置 utf-8，否则server会报 unicode error。若后设置utf-8，保存后中文也是乱码。
        开始进行查找前我们先来认识filter()方法。 
        这是一个过滤器方法用于过滤掉不符合条件的元素。 
        值得一提的是其内自带方法函数的引用方式为‘__方法名称’。（两个下划线） 
        __exact 精确等于 like ‘aaa’ 
        __iexact 精确等于 忽略大小写 ilike ‘aaa’ 
        __contains 包含 like ‘%aaa%’ 
        __icontains 包含 忽略大小写 ilike ‘%aaa%’，但是对于sqlite来说，contains的作用效果等同于icontains。 
        __gt 大于 
        __gte 大于等于 
        __lt 小于 
        __lte 小于等于 
        __in 存在于一个list范围内 
        __startswith 以…开头 
        __istartswith 以…开头 忽略大小写 
        __endswith 以…结尾 
        __iendswith 以…结尾，忽略大小写 
        __range 在…范围内 
        __year 日期字段的年份 
        __month 日期字段的月份 
        __day 日期字段的日 
        __isnull=True/False 
    '''
