from django.contrib import admin
from django.contrib.auth.models import Group

from .models import PsihoTest, AssignedTest, Question, Answer, AnswerTest, UserProfile


class AnswerC(admin.ModelAdmin):
    list_display = ('id', 'text', 'score')
    list_filter = ('text', )
    list_display_links = ['text']
    fieldsets = (
        (None, {
            'fields': ( ('text', 'score'),)
        }),)

class AnswerInline(admin.StackedInline):
    model = Question.answers.through

class QuestionC(admin.ModelAdmin):
    list_display = ('id', 'text', 'raspunsuri')
    # filter_vertical = ('answers',)
    list_display_links = ['text']
    fieldsets = [
        ('Intrebari', {
            'fields': ['text', ]
         }
        ),
    ]
    inlines = (AnswerInline, )

    def raspunsuri(self, obj):
        return " | ".join([f"{q.text} - {q.score}" for q in obj.answers.all()])

class AnswerTestC(admin.ModelAdmin):
    list_display = ('id', 'question', 'choose')
    list_display_links = ['question']
    fieldsets = (
        (None, {
            'fields': ( 'question', 'choose',)
        }),)

class AnswerTestInline(admin.StackedInline):
    model = AssignedTest.answer.through

class AssignedC(admin.ModelAdmin):
    list_display = ('id', 'name', 'completat', 'data', 'psihotest', 'email', 'message')
    search_fields = ('name', )
    list_display_links = ['name']
    list_filter = ('data', 'email')
    fieldsets = (
        ('Atribuire', {
            'fields': ( ('name', 'email'), ('psihotest', 'data'), 'message',)
        }),)
    inlines = (AnswerTestInline,)

    def completat(self, obj):
        return 'Da' if obj.answer.all() else 'Nu'

class QuestionInline(admin.StackedInline):
    model = PsihoTest.questions.through

class PsihoC(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ('text', )
    list_display = ('id', 'text',)
    list_display_links = ['text']
    filter_vertical = ('questions',)

    fieldsets = [
        ('Test', {
            'fields': ['text', 'story']
         }
        ),
        # ('Intrebari', {
        #     'fields': ['questions', ],
        #     'classes': ['collapse']
        # })
    ]
    inlines = (QuestionInline, )

    # def intrebari(self, obj):
    #     return " | ".join([q.text for q in obj.questions.all()])

class UserProfileC(admin.ModelAdmin):
    list_display = ('user', 'teste')
    # filters
    #list_filter = ('first_name', )

    def teste(self, obj):
        return " | ".join([q.text for q in obj.user_test.all()])

# Registred models.
admin.site.register(AssignedTest, AssignedC)
admin.site.register(PsihoTest, PsihoC)
admin.site.register(AnswerTest, AnswerTestC)
admin.site.register(Question, QuestionC)
admin.site.register(Answer, AnswerC)
admin.site.register(UserProfile, UserProfileC)

admin.site.unregister(Group)

# Admin page title
admin.site.site_header = "Administrarea testelor"