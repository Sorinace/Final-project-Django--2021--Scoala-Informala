from django.db import models
from django.contrib.postgres.fields import ArrayField

class Answer(models.Model):
  text = models.CharField(max_length=200)
  score =models.IntegerField()
  objects = None # For the error:Class '<class name>' has no 'objects' memberpylint(no-member) in View

  def __str__(self):
    return f"Answer is: {self.text} with score {self.score}" 

class Question(models.Model):
  text = models.CharField(max_length=200)
  answers = models.ManyToManyField(Answer) 
  objects = None # For the error:Class '<class name>' has no 'objects' memberpylint(no-member) in View
  
  def __str__(self):
    return f"Qestion is: {self.text} " 

class PsihoTest(models.Model):
  text = models.CharField(max_length=100)
  story = models.TextField()
  questions = models.ManyToManyField(Question)
  total_score = ArrayField(ArrayField(models.IntegerField()), null=True, blank=True)

  def __str__(self):
        return f"Quiz name is: {self.text} " 

class AnswerTest(models.Model):
  question = models.ForeignKey(Question,  on_delete=models.DO_NOTHING, null=True, blank=True)
  choose = models.ForeignKey(Answer,  on_delete=models.DO_NOTHING, null=True, blank=True)

  objects = None # For the error:Class '<class name>' has no 'objects' memberpylint(no-member) in View
  
  def __str__(self):
    return f"{self.question}, {self.choose} " 


class AssignedTest(models.Model):
  psihotest = models.ForeignKey(PsihoTest, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  email = models.EmailField()
  data =  models.DateField() 
  message = models.CharField(max_length=200, null=True, blank=True)
  answer = models.ManyToManyField(AnswerTest, blank=True)
  
  objects = None # For the error:Class '<class name>' has no 'objects' memberpylint(no-member) in View

  def __str__(self):
        return f"Quiz was assigned to the {self.name}, and is valid until {self.data} "
