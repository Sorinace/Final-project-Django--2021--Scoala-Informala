from query.models import AnswerTest, AssignedTest, Question
from django.contrib.auth import models
from rest_framework import serializers

from query.models import AssignedTest, PsihoTest, AnswerTest, Question, Answer


class AnswerTestSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnswerTest
        fields = '__all__'


class AnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('text', )


class QuestionSerializers(serializers.ModelSerializer):
    answers = AnswerSerializers(many = True)

    class Meta:
        model = Question
        fields = '__all__'


class PsihoTestSerializers(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializers(many = True)

    class Meta:
        model = PsihoTest
        fields = '__all__' # ('id', 'text', 'story', 'questions', )


class AssignedSerializers(serializers.ModelSerializer):
    # psihotest = PsihoTestSerializers()

    class Meta:
        model = AssignedTest
        fields = ('id', 'data', 'message', 'email',)