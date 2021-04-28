from django.shortcuts import render
from django.http import HttpResponse
from .models import PsihoTest, AssignedTest
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId

@csrf_exempt
def query(request):
  # e = PsihoTest.objects.create(
  #   text='test',
  #   story='This is how we supposed to feel this questionare ....',
  #   questions=[{
  #       'text': 'Ce faci?',
  #       'answers': [{
  #           'text': 'bine!',
  #           'score': 1
  #         }, {
  #           'text': 'Foarte bine!',
  #           'score': 2
  #         }, {
  #           'text': 'Excelent!',
  #           'score': 3
  #         }
  #       ]
  #   }, {
  #     'text': 'Cum o mai duci?',
  #       'answers': [{
  #           'text': 'bine!',
  #           'score': 1
  #         },{
  #           'text': 'Foarte bine!',
  #           'score': 2
  #         }, {
  #           'text': 'Excelent!',
  #           'score': 3
  #         }
  #       ]
  #   }]
  #   )
  
  # e = AssignedTest.objects.create(
  #   psihotest = psihotest._id,
  #   text = 'Nicu Alexandru',
  #   email = 'email@email.com',
  #   data = '2021-05-25',
  #   message = 'Ceva ce vreau sa transmit ... daca e cazul',
  #   answer = []
  # )

  assigned = AssignedTest.objects.get(text = 'Nicu Alexandru')
  psihotest = PsihoTest.objects.get(_id= ObjectId(assigned.psihotest))


  if request.method == 'GET':
    return render(request, 'query/query.html', {'psihotest': psihotest})
  elif request.method == 'POST':
    return HttpResponse(psihotest.questions)
def home(request):
  return render(request, 'base.html')

import datetime
def about(request):
    time = datetime.datetime.now()
    return render(request, 'about.html',{'time': time})