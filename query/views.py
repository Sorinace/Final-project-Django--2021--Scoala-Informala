import datetime

from rest_framework.decorators import api_view
from django.contrib import messages #import messages
from django.shortcuts import render

from .models import PsihoTest, AssignedTest, AnswerTest, Question, Answer
from .forms import AssignPsihoTest
from .email import sendEmail, sendEmailAnswer
from .errors import MyException, notValid, notCopleted, notSaved, toLate

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
      return notCopleted()
  except MyException:
    return notCopleted()
  return True

@api_view(['GET'])
def query(request, id='1'):
  try:
    assigned = AssignedTest.objects.get(id=id)
    psihotest = assigned.psihotest 
    # check if the test is completed or not
    if (len(assigned.answer.all()) > 0):
      messages.info(request, 'Acest test a fost deja completat!')
      psihotest = None
      id = None
    elif(assigned.data < datetime.date.today()):
      toLate()
  except  Exception as e:
    messages.info(request, e)
  return render(request, 'query.html', {'psihotest': psihotest, 'id': id})

def home(request):
  return render(request, 'base.html')

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
      base = "{0}://{1}".format(request.scheme, request.get_host())
      try:
        asignTest.save()
        if (asignTest.id):
          pass
          sendEmail(request, 'Atribuire test', asignTest.email, 'Diana Avram', f"{base}/query/{asignTest.id}" , asignTest.data, asignTest.message)
        else:
          notSaved()
      except Exception as e:
        return e
      return render(request, 'save.html')
    else:
      notValid()    
  # if is GET
  else:
    form = AssignPsihoTest()
  return render(request, 'asign.html', {'form': form})

@api_view(['GET', 'POST'])
def asigned(request):
  if request.method == 'POST':
    # for i in request.POST:
    print(request.POST)
    assigned = []
    if ('assign' in request.POST):
      assign = request.POST['assign']
    else:
      assign = 'Nu ai selectat nimic'
    text_option = ['Nu ai ales nimic', 'Modifica', 'Sterge']
    text = f"{text_option[int(request.POST['option'])]} - {assign}"
    assigned = AssignedTest.objects.all()#get(id='1')
  else:
    assigned = AssignedTest.objects.all()
    text = ''
  return render(request, 'asigned.html', {'assigned': assigned, 'text': text})

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


def about(request):
  return render(request, 'about.html')