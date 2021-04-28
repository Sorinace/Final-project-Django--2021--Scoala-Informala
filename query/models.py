from djongo import models

class Answer(models.Model):
    text = models.CharField(max_length=255)
    score = models.IntegerField

    class Meta:
        abstract = True

class Question(models.Model):
    text = models.CharField(max_length=500)
    answers = models.ArrayField( 
            model_container = Answer
        )

    class Meta:
        abstract = True

class PsihoTest(models.Model):
    _id = models.ObjectIdField()
    text = models.CharField(max_length=100)
    story = models.TextField()
    questions = models.ArrayField( 
            model_container = Question
        )
    total_rules = models.JSONField()
    objects = models.DjongoManager()

class AssignedTest(models.Model):
    _id = models.ObjectIdField()
    psihotest = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    email = models.EmailField()
    data = models.DateField() # YYYY-MM-DD
    message = models.TextField()
    answer = models.JSONField()
    objects = models.DjongoManager()