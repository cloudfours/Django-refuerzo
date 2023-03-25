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
        return self.published_date >= timezone.now() - datetime.timedelta(days=1)
class Choices(models.Model):
    question = models.ForeignKey("Question", null=True, on_delete=models.CASCADE,related_name="question_choice")
    choice_text=models.CharField(max_length=30,default=None)
    votes=models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
        