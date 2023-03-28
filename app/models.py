import datetime
from django.db import models
from django.utils import timezone
# Create your models here.
class Question(models.Model):
    question_text=models.CharField(max_length=30,default=None)
    pub_date=models.DateTimeField("date published")
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def present_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def past_published_recently(self):
        return  timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    # def save(self,*args, **kwargs):
    #      super().save(*args,**kwargs)
    #      if self.question_choice.all().count() == 0:
    #          super().delete()
    #          raise Exception('deberia tener almenos un opcion no puede estar vacio')
class Choices(models.Model):
    question = models.ForeignKey("Question", null=True, on_delete=models.CASCADE,related_name="question_choice")
    choice_text=models.CharField(max_length=30,default=None)
    votes=models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
   
       
        