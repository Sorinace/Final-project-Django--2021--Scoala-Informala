from djongo import models

# into admin.py I added for registration of model in admin panel

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
    total_rules = []
    objects = models.DjongoManager()

#  e = PsihoTest.objects.create(
#     text='test',
#     story='This is how we supposed to feel this questionare ....',
#     questions=[{
#         'text': 'Ce faci?',
#         'answers': [{
#             'text': 'bine!',
#             'score': 1
#           }, {
#             'text': 'Foarte bine!',
#             'score': 2
#           }, {
#             'text': 'Excelent!',
#             'score': 3
#           }
#         ]
#     }, {
#       'text': 'Cum o mai duci?',
#         'answers': [{
#             'text': 'bine!',
#             'score': 1
#           },{
#             'text': 'Foarte bine!',
#             'score': 2
#           }, {
#             'text': 'Excelent!',
#             'score': 3
#           }
#         ]
#     }]
#     )

# g = PsihoTest.objects.get(text='test')
# assert e == g
