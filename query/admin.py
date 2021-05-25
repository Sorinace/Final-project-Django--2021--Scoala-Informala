from django.contrib import admin
from django.contrib.auth.models import Group

from .models import PsihoTest, AssignedTest, Question, Answer, AnswerTest

# ModelAdmin Class # DataFlair
class AnswerC(admin.ModelAdmin):
    # exclude = ('score', )
    list_display = ('id', 'text', 'score')
    # filters
    list_filter = ('text', )

class QuestionC(admin.ModelAdmin):
    # exclude = ('score', )
    list_display = ('id', 'text', 'raspunsuri')

    def raspunsuri(self, obj):
        return " | ".join([f"{q.text} - {q.score}" for q in obj.answers.all()])


class AssignedC(admin.ModelAdmin):
    # exclude = ('score', )
    list_display = ('id', 'completat', 'name', 'data', 'psihotest', 'email', 'message')
    # filters
    list_filter = ('data', 'name', 'email')

    def completat(self, obj):
        return 'Nu' if obj.answer else 'Da'

class PsihoC(admin.ModelAdmin):
    # exclude = ('score', )
    list_display = ('id', 'text', 'intrebari')
    # filters
    list_filter = ('text', )

    def intrebari(self, obj):
        return " | ".join([q.text for q in obj.questions.all()])

# Registred models.
admin.site.register(AssignedTest, AssignedC)
admin.site.register(PsihoTest, PsihoC)
admin.site.register(AnswerTest)
admin.site.register(Question, QuestionC)
admin.site.register(Answer, AnswerC)

admin.site.unregister(Group)

# Admin page title
admin.site.site_header = "Administrarea testelor"