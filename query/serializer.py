from rest_framework import serializers
from .models import PsihoTest, AssignedTest, Answer, Question, AnswerTest

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('id', 'text')

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'answers')

class PsihoTestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = PsihoTest
        fields = ('id', 'text', 'story', 'questions')

class AnswerTestSerializer(serializers.ModelSerializer):
  
  class Meta:
        model = AnswerTest
        fields = ('question', 'choose')

class AssignedTestSerializer(serializers.ModelSerializer):
    psihotest = PsihoTestSerializer()
    answer = AnswerTestSerializer()

    class Meta:
        model = AssignedTest
        fields = ('id', 'name', 'email', 'data', 'message', 'psihotest', 'answer')

