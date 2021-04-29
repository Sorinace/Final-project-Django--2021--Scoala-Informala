from django.shortcuts import render
from django.http import HttpResponse
from .models import PsihoTest, AssignedTest
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId

@csrf_exempt
def query(request):
  # e = PsihoTest.objects.create(
  #   text='PsihoTest',
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
  #   }],
  #   total_rules = []
  #   )
  
  # e = AssignedTest.objects.create(
  #   psihotest = psihotest._id,
  #   text = 'Ticu',
  #   email = 'email2@email.com',
  #   data = '2021-05-25',
  #   message = 'Ceva ce vreau sa transmit ... daca NU e cazul',
  #   answer = []
  # )

  assigned = AssignedTest.objects.get(text = 'Ticu')
  psihotest = PsihoTest.objects.get(_id= ObjectId(assigned.psihotest))
  if request.method == 'GET':
    print(psihotest.text)
    return render(request, 'query/query.html', {'psihotest': psihotest})
  elif request.method == 'POST':
    return HttpResponse([psihotest.questions, assigned.text])
def home(request):
  return render(request, 'base.html')

import datetime
def about(request):
    time = datetime.datetime.now()
    return render(request, 'about.html',{'time': time})