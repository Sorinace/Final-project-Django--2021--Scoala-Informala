from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import PsihoTest, AssignedTest, AnswerTest, Question, Answer
from .serializer import PsihoTestSerializer, AssignedTestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

# from django.views.decorators.csrf import csrf_exempt 

def saveAnswer(answers):
  # score = AnswerTest
  try:
    assigned = AssignedTest.objects.get(id=answers['id'])
    for ans in answers['answers']:
      score = AnswerTest(question = Question.objects.get(id=ans['question']),
        choose = Answer.objects.get(id=ans['choose']))
      print(score)
      score.save()
      assigned.answer.add(score)
  except Exception as e:
    return e
  return True

# @csrf_exempt
@api_view(['GET'])
def query(request, id='1'):
  if request.method == 'GET':
    assigned = AssignedTest.objects.get(id=id)
    serializer = AssignedTestSerializer(assigned)
    return Response(serializer.data)

@api_view(['POST'])
def answer(request):
  try:
    answers = json.loads(request.body.decode("utf-8"))
    saveAnswer(answers)
    
  except Exception as e:
    print(f"Type: {type(e)}")
    return Response(False)
  return Response(True)

def home(request):
  return render(request, 'base.html')

import datetime
def about(request):
    time = datetime.datetime.now()
    return render(request, 'about.html',{'time': time})