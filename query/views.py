from django.shortcuts import render
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from .models import PsihoTest, AssignedTest, AnswerTest, Question, Answer
from .forms import AssignPsihoTest
from .email import sendEmail, sendEmailAnswer
from .serializer import AssignedTestSerializer
from .errors import MyException, incomplet
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from django.contrib import messages #import messages

def saveAnswer(request, answers):
  try:
    assigned = AssignedTest.objects.get(id=answers['id'])
    if(len(answers['answers']) == len(assigned.psihotest.questions.all())):
      for ans in answers['answers']:
        score = AnswerTest(question = Question.objects.get(id=ans['question']), choose = Answer.objects.get(id=ans['choose']))
        score.save()
        assigned.answer.add(score)
      sendEmailAnswer(request, assigned)
    else:
      incomplet()
  except MyException:
    return incomplet()
  return True

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
  # messages.success(request, "Test valid!" )
  # check if the test is completed or not
  if (len(assigned.answer.all()) > 0):
    messages.info(request, 'Acest test a fost deja completat!')
    psihotest = None
    id = None
  return render(request, 'query.html', {'psihotest': psihotest, 'id': id})

@api_view(['GET', 'POST'])
def asign(request):
  if request.method == 'POST':
    # create a form instance and populate it with data from the request:
    form = AssignPsihoTest(request.POST)
    # check whether it's valid:
    if form.is_valid():
      # process the data in form.cleaned_data as required
      asignTest = AssignedTest()
      asignTest.psihotest = PsihoTest.objects.get(text=form.cleaned_data['psihotest'])
      asignTest.name =  form.cleaned_data['name']
      asignTest.email =  form.cleaned_data['email']
      asignTest.data = form.cleaned_data['data']
      asignTest.message = form.cleaned_data['message']
      print(asignTest)
      try:
      #   asignTest.save()
        sendEmail(request, 'Atribuire test', asignTest.email, 'Diana Avram', f"http://localhost:8000/query/{asignTest.id}", asignTest.data, asignTest.message)
        # emailAssignedTest( asignTest.email, f"http://localhost:8000/query/{asignTest.id}", asignTest.data, asignTest.message)
      except Exception as e:
        return e
      # redirect to a new URL:
      return HttpResponseRedirect('/about/')
    else:
      print('NU merge?') # raise a error the form is not valid
      print(form)
    # if a GET (or any other method) we'll create a blank form
    
  else:
    form = AssignPsihoTest()
  return render(request, 'asign.html', {'form': form})

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
  try:
    saveAnswer(request, answers)
  except MyException as e:
    print(e)
    messages.info(request, e)
  return render(request, 'save.html')

def home(request):
  return render(request, 'base.html')

import datetime
def about(request):
  # emailAssignedTest('sorinace@gmail.com', 'http://localhost:8000/query/2', data, mesaj)
  time = datetime.datetime.now()
  # sendEmail(request, 'Atribuire test','sorinace@gmail.com', 'Diana Avram', 'http://localhost:8000/query/2', time, "mesaj catre TARA")
  return render(request, 'about.html',{'time': time})