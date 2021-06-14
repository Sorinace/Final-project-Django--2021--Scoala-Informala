from django.contrib import admin
from django.contrib.auth.models import Group

from .models import PsihoTest, AssignedTest, Question, Answer, AnswerTest, UserProfile

# ModelAdmin Class # DataFlair
class AnswerC(admin.ModelAdmin):
    # exclude = ('score', )
    list_display = ('id', 'text', 'score')
    # filters
    list_filter = ('text', )
    fieldsets = (
        (None, {
            'fields': ( ('text', 'score'),)
        }),)

class QuestionC(admin.ModelAdmin):
    list_display = ('id', 'text', 'raspunsuri')
    filter_vertical = ('answers',)

    def raspunsuri(self, obj):
        return " | ".join([f"{q.text} - {q.score}" for q in obj.answers.all()])


class AssignedC(admin.ModelAdmin):
    list_display = ('id', 'name', 'completat', 'data', 'psihotest', 'email', 'message')
    search_fields = ('name', )
    list_display_links = ['name']
    # filters
    list_filter = ('data', 'email')

    def completat(self, obj):
        return 'Da' if obj.answer.all() else 'Nu'

class PsihoC(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ('text', )
    list_display = ('id', 'text', 'intrebari')
    list_display_links = ['text']
    filter_vertical = ('questions',)
    # filters
    # list_filter = ('text', 'questions')


    fieldsets = [
        ('Test', {
            'fields': ['text', 'story']
         }
        ),
        ('Intrebari', {
            'fields': ['questions', ],
            'classes': ['collapse']
        })
    ]

    def intrebari(self, obj):
        return " | ".join([q.text for q in obj.questions.all()])

class UserProfileC(admin.ModelAdmin):
    list_display = ('user', 'teste')
    # filters
    #list_filter = ('first_name', )

    def teste(self, obj):
        return " | ".join([q.text for q in obj.user_test.all()])

# Registred models.
admin.site.register(AssignedTest, AssignedC)
admin.site.register(PsihoTest, PsihoC)
admin.site.register(AnswerTest)
admin.site.register(Question, QuestionC)
admin.site.register(Answer, AnswerC)
admin.site.register(UserProfile, UserProfileC)

admin.site.unregister(Group)

# Admin page title
admin.site.site_header = "Administrarea testelor"