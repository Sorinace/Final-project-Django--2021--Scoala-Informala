import datetime

from rest_framework.decorators import api_view
from django.contrib import messages 
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from .models import PsihoTest, AssignedTest, AnswerTest, Question, Answer, UserProfile
from .forms import AssignPsihoTest
from .email import sendEmail, sendEmailAnswer, sendEmailRemainder
from .errors import MyException, notValid, notCopleted, notSaved, toLate, done, sendError

def saveAnswer(request, answers):
  try:
    assigned = AssignedTest.objects.get(id=answers['id'])
    if(len(answers['answers']) == len(assigned.psihotest.questions.all())):
      for ans in answers['answers']:
        score = AnswerTest(question = Question.objects.get(id=ans['question']), choose = Answer.objects.get(id=ans['choose']))
        score.save()
        assigned.answer.add(score)
      
      # get the user who assigned the test
      assign_user = assigned.userprofile_set.all()[0]
      # get his/her e-mail address
      email = User.objects.filter(username=assign_user).values_list('email', flat=True)[0] 
      sendEmailAnswer(request, assigned, email)
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
    # check if the test is in time
    if(assigned.data < datetime.date.today()):
      toLate()
    # check if the test is completed or not
    elif (len(assigned.answer.all()) > 0):
      done()
    return render(request, 'query.html', {'psihotest': psihotest, 'id': id})
  except  Exception as e:
    messages.info(request, e)
  return render(request, 'query.html', {'page_obj': None, 'story': '', 'name': '', 'id': id})

def home(request):
  # sendEmailRemainder()
  return render(request, 'base.html')

@api_view(['GET', 'POST'])
def asign(request):
  if request.method == 'POST':
    # create a form instance and populate it with data from the request:
    form = AssignPsihoTest(request.POST)
    # check whether it's valid:
    if form.is_valid():
      # process the data in form.cleaned_data as require
      if (int(request.POST['id']) < 1):
        asignTest = AssignedTest()
      else:
        asignTest = get_object_or_404(AssignedTest, id=request.POST['id'])
      asignTest.psihotest = get_object_or_404(PsihoTest, text = form.cleaned_data['psihotest'].text)
      asignTest.name =  form.cleaned_data['name']
      asignTest.email =  form.cleaned_data['email']
      asignTest.data = form.cleaned_data['data']
      asignTest.message = form.cleaned_data['message']
      try:
        asignTest.save()
        # add test to user
        user = UserProfile.objects.get(user = request.user)
        user.user_assign.add(asignTest)
        if (asignTest.id):
          base = "{0}://{1}".format(request.scheme, request.get_host())
          sendEmail(request, 'Atribuire test', asignTest.email, f"{base}/query/{asignTest.id}" , asignTest.data, asignTest.message)
        else:
          notSaved()
      except Exception as e:
        sendError(e)
      return render(request, 'save.html')
    else:
      notValid()
  # if is GET
  else:
    form = AssignPsihoTest()
    title = 'Atribuie test!'
    if (request.user.is_anonymous):
      psihotest = None
    else:
      # Assign the choices based on User
      form.fields['psihotest'].queryset = UserProfile.objects.get(user = request.user).user_test.all()
      user = UserProfile.objects.get(user = request.user)
      psihotest = user.user_test.all()
  return render(request, 'asign.html', {'form': form, 'title': title, 'model': None, 'id': -1, 'psihotest': psihotest})

@api_view(['GET', 'POST'])
def asigned(request):
  if request.method == 'POST':
    if ('assign' in request.POST and 'option' in request.POST):
      text_option = ['Nu ai selectat nimic', 'Modifica', 'Sterge', 'Retrimite e-mail']
      text = f"{text_option[int(request.POST['option'])]} pentru ID: {request.POST['assign']}"
      if (int(request.POST['assign']) > 0):
        assigned = []
        assigned.append( AssignedTest.objects.get(id=request.POST['assign']) )
        if (request.POST['option'] == '1'):
          form = AssignPsihoTest()
          model = get_object_or_404(AssignedTest, id=request.POST['assign'])
          title = 'Modifica atribuire test!'
          return render(request, 'asign.html', {'form': form, 'title': title, 'model': model, 'id': request.POST['assign']})
        elif (request.POST['option'] == '2'):
          return render(request, 'asigned-delete.html', { 'assigned': assigned[0], 'id': int(request.POST['assign'])})
        elif (request.POST['option'] == '3'):
           base = "{0}://{1}".format(request.scheme, request.get_host())
           asignTest = get_object_or_404(AssignedTest, id=request.POST['assign'])
           sendEmail(request, 'Nu uita, ai un test atribuit', asignTest.email, f"{base}/query/{asignTest.id}" , asignTest.data, asignTest.message)
           text = f"Email trimis pentru {asignTest.name}, la adresa {asignTest.email}"
    else:
      text = ''
      
  else:
    text = ''
  if (request.user.is_anonymous):
    page_obj = None
  else:
    user = UserProfile.objects.get(user = request.user)
    assigned = user.user_assign.all()
    paginator = Paginator(assigned, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
  return render(request, 'asigned.html', {'page_obj': page_obj, 'text': text, 'date': datetime.date.today()})

@api_view(['POST'])
def asigned_delete(request):
  remove = get_object_or_404(AssignedTest, id=request.POST['id'])
  remove.delete()
  return redirect('asigned')

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