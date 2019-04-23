# -*- coding:utf-8 -*-

from django.shortcuts import render,get_object_or_404
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
#from django.views.generic import TemplateView
from .models import Question,Choice
from django.utils import timezone
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage,InvalidPage


# Create your views here.

'''
关于：使用 TemplateView
'''
class AboutView(generic.TemplateView):
    template_name = 'polls/about.html'

'''
显示问题及选项：使用 DetailView
'''
class DetailView(generic.DetailView):
    #template_name = 'polls/detail.html' # 不指定则自动找默认规则的页面 <model name>_detail.html。By default, the DetailView generic view uses a template called <app name>/<model name>_detail.html.
    model = Question # 必须指定model，对应的question将自动作为context字典的一部分。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vote_time'] = timezone.now() # override default context,and append your own elements in it.
        return context

# def detail(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/detail.html',{'question':question})
#     #return HttpResponse("Question %s" %question_id)

'''
查看投票结果
'''
class ResultsView(generic.DetailView):
    template_name = 'polls/results.html'# 如果这里不指定，则默认为question_detail.html,参见上面的DetailView实现。
    model = Question
    
# def results(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/results.html',{'question':question})
#     #return HttpResponse("The results of question %s" %question_id)


'''
首页，列表显示投票问题：使用 ListView
'''
class IndexView1(generic.ListView):
    template_name = 'polls/index.html' # the ListView generic view uses a default template called <app name>/<model name>_list.html
    context_object_name = 'latest_question_list' #默认为 <model name>_list，或直引用 object_list，这里override默认变量
    #all_list = Question.objects.order_by('-pub_date')
    def get_queryset(self):
        all_list = Question.objects.order_by('pub_date')
        return all_list #返回的all_list对象在页面中以context_object_name变量定义的名称访问
    

'''
首页，列表显示投票问题：使用 TemplateView （效果同上面的 ListView,实际上ListView继承自TemplateView）
'''
class IndexView2(generic.TemplateView):
    template_name = 'polls/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_question_list'] = Question.objects.order_by('-pub_date')[:3]
        return context
    
def index(request):
    #return HttpResponse("Hello,world.You're at the polls index.")
    question_list = Question.objects.order_by('pub_date')
    #latest_question_list = Question.objects.filter(question_text__icontains='what').order_by('-pub_date')[:5] # 模糊查询，按时间倒序取前5
    paginator = Paginator(question_list,3)
    #print(paginator.num_pages)
    page = request.GET.get('page')
    #     try:
    #         latest_question_list = paginator.page(page)
    #     except (PageNotAnInteger,InvalidPage):
    #         latest_question_list = paginator.page(1)
    #     except EmptyPage:
    #         latest_question_list = paginator.page(paginator.num_pages)
    latest_question_list = paginator.get_page(page) #异常时自动首页或末页，get_page与page方法的区别
    
    return render(request,'polls/index.html',{'latest_question_list':latest_question_list})


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
        return render(request, 'polls/question_detail.html', {'question':question,'error_message':'您没有选择！'})
    except Choice.DoesNotExist:
        return render(request, 'polls/question_detail.html', {'question':question,'error_message':'您没有选择！！'})
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
        

