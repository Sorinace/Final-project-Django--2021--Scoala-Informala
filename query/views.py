from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import PsihoTest, AssignedTest
from .serializer import PsihoTestSerializer, AssignedTestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# from django.views.decorators.csrf import csrf_exempt 


# @csrf_exempt
@api_view(['GET'])
def query(request, id):
  if request.method == 'GET':
    assigned = AssignedTest.objects.get(id=id)
    serializer = AssignedTestSerializer(assigned)
    return Response(serializer.data)

def home(request):
  return render(request, 'base.html')

import datetime
def about(request):
    time = datetime.datetime.now()
    return render(request, 'about.html',{'time': time})