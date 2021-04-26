from django.shortcuts import render
from django.http import HttpResponse
from .models import PsihoTest

def query(request):
  psihotest = 'Se transmite textul in pagina!'
 
  return render(request, 'query/index.html', {'psihotest': psihotest})