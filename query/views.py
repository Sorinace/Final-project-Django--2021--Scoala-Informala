from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import PsihoTest, AssignedTest, AnswerTest, Question, Answer
from .email import emailAssignedTest
from .serializer import PsihoTestSerializer, AssignedTestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

# from django.views.decorators.csrf import csrf_exempt 

def saveAnswer(answers):
  try:
    assigned = AssignedTest.objects.get(id=answers['id'])
    for ans in answers['answers']:
      score = AnswerTest(question = Question.objects.get(id=ans['question']), choose = Answer.objects.get(id=ans['choose']))
      score.save()
      assigned.answer.add(score)
      # print(score)
  except Exception as e:
    return e
  return True

# @csrf_exempt
@api_view(['GET'])
def query_api(request, id='1'):
  if request.method == 'GET':
    assigned = AssignedTest.objects.get(id=id)
    serializer = AssignedTestSerializer(assigned)
    return Response(serializer.data)

@api_view(['GET'])
def query(request, id='1'):
  assigned = AssignedTest.objects.get(id=id)
  psihotest = assigned.psihotest 
  return render(request, 'query/query.html', {'psihotest': psihotest, 'id': id})

@api_view(['POST'])
def answer_api(request):
  try:
    answers = json.loads(request.body.decode("utf-8"))
    saveAnswer(answers)
    
  except Exception as e:
    print(f"Type: {type(e)}")
    return Response(False)
  return Response(True)

@api_view(['POST'])
def answer(request):
  item = {}
  answers= {}
  answer=[]
  for i in request.POST:
    if i == 'id':
      answers['id'] = int(request.POST[i])
    elif i != 'csrfmiddlewaretoken':
      item['question'] = int(i)
      item['choose'] = int(request.POST[i])
      answer.append(item)
      item = {}
  answers["answers"] = answer
  # print(answers)
  saveAnswer(answers)
  return render(request, 'save.html')

def home(request):
  return render(request, 'base.html')

import datetime
def about(request):
  # emailAssignedTest('sorinace@gmail.com', 'http://localhost:8000/query/2')
  time = datetime.datetime.now()
  return render(request, 'about.html',{'time': time})