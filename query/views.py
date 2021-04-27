from django.shortcuts import render
from django.http import HttpResponse
from .models import PsihoTest

def query(request):
  psihotest = PsihoTest.objects.create(
    text='test',
    story='This is how we supposed to feel this questionare ....',
    questions=[{
        'text': 'Ce faci?',
        'answers': [{
            'text': 'bine!',
            'score': 1
          }, {
            'text': 'Foarte bine!',
            'score': 2
          }, {
            'text': 'Excelent!',
            'score': 3
          }
        ]
    }, {
      'text': 'Cum o mai duci?',
        'answers': [{
            'text': 'bine!',
            'score': 1
          },{
            'text': 'Foarte bine!',
            'score': 2
          }, {
            'text': 'Excelent!',
            'score': 3
          }
        ]
    }]
    )
 
  return render(request, 'query/query.html', {'psihotest': psihotest})

def home(request):
  return render(request, 'base.html')

import datetime
def about(request):
    time = datetime.datetime.now()
    return render(request, 'about.html',{'time': time})