from query.models import AnswerTest, AssignedTest, Question
from django.contrib.auth import models
from rest_framework import serializers

from query.models import AssignedTest, PsihoTest, AnswerTest, Question, Answer


class AnswerTestSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnswerTest
        fields = '__all__'


class AnswerSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ('text', 'score')


class QuestionSerializers(serializers.ModelSerializer):
    answers = AnswerSerializers(many = True)

    class Meta:
        model = Question
        fields = '__all__'


class PsihoTestSerializers(serializers.ModelSerializer):
    questions = QuestionSerializers(many = True)

    class Meta:
        model = PsihoTest
        fields = ('id', 'text', 'story', 'questions', )


class AssignedSerializers(serializers.HyperlinkedModelSerializer):
    # psihotest = PsihoTestSerializers()

    class Meta:
        model = AssignedTest
        fields = ('id', 'data', 'message', 'email', 'psihotest',)