from django.db import models
from django.contrib.postgres.fields import ArrayField

class Answer(models.Model):
  text = models.CharField(max_length=200)
  score =models.IntegerField()

class Question(models.Model):
  text = models.CharField(max_length=200)
  answers = models.ManyToManyField(Answer) 

class PsihoTest(models.Model):
  text = models.CharField(max_length=100)
  story = models.TextField()
  questions = models.ManyToManyField(Question)
  total_score = ArrayField(ArrayField(models.IntegerField()))

  def __str__(self):
        return f"Quiz name is: {self.text} " 


class AssignedTest(models.Model):
  psihotest = models.ForeignKey(PsihoTest, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  email = models.EmailField()
  data =  models.DateField() 
  message = models.CharField(max_length=200)
  answer = ArrayField(models.IntegerField())

  def __str__(self):
        return f"Quiz was assigned to the {self.name} "
