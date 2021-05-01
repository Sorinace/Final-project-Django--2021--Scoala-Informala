from mongoengine import * 

class Answer(EmbeddedDocument):
  text = StringField(required=True)
  score =IntField(required=True)

class Question(EmbeddedDocument):
  text = StringField(required=True)
  answers = EmbeddedDocumentListField(Answer)

class PsihoTest(Document):
  text = StringField(required=True, max_length=100)
  story = StringField(required=True)
  questions = EmbeddedDocumentListField(Question)
  total_score = ListField(ListField(IntField()))


class AssignedTest(Document):
  psihotest = ReferenceField(PsihoTest, reverse_delete_rule=CASCADE)
  name = StringField(required=True)
  email = StringField(required=True)
  data =  DateTimeField(required=True) # Uses the python-dateutil library
  message = StringField()
  answer = ListField(IntField())
