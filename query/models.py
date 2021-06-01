from django.db import models
from django.contrib.postgres.fields import ArrayField

class Answer(models.Model):
  text = models.CharField(max_length=200)
  score = models.IntegerField()
    
  class Meta:
    ordering = ['-text']
  
  def __str__(self):
    return f"{self.id} - {self.text} cu punctajul = {self.score}" 

class Question(models.Model):
  text = models.CharField(max_length=200)
  answers = models.ManyToManyField(Answer) 
    
  def __str__(self):
    return f"{self.id} - {self.text} " 

class PsihoTest(models.Model):
  text = models.CharField(max_length=100)
  story = models.TextField()
  questions = models.ManyToManyField(Question)
  total_score = ArrayField(ArrayField(models.IntegerField()), null=True, blank=True)
  
  def __str__(self):
        return f"{self.id} - {self.text} " 

class AnswerTest(models.Model):
  question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, null=True, blank=True)
  choose = models.ForeignKey(Answer, on_delete=models.DO_NOTHING, null=True, blank=True)

  def __str__(self):
    return f"{self.id} - {self.question}, {self.choose} " 


class AssignedTest(models.Model):
  psihotest = models.ForeignKey(PsihoTest, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  email = models.EmailField()
  data =  models.DateField() 
  message = models.CharField(max_length=200, null=True, blank=True)
  answer = models.ManyToManyField(AnswerTest, blank=True)
  
  def __str__(self):
        return f"{self.psihotest.text} - a fost atribuit lui {self.name}, si este valid pana in {self.data} "
  class Meta:
    ordering = ['-data']