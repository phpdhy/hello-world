# -*- coding:utf-8 -*-

from django.db import models
# from django.utils.text import slugify

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date_published')
#     slug = models.SlugField(max_length=50)
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.question_text)
#         super(Question, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.question_text
    
class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    
