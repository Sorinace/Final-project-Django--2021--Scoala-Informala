from django.contrib import admin
from .models import PsihoTest, AssignedTest, Question, Answer, AnswerTest

# Register your models here.

admin.site.register(AssignedTest)
admin.site.register(PsihoTest)
admin.site.register(AnswerTest)
admin.site.register(Question)
admin.site.register(Answer)
