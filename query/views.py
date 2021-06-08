import datetime

from access_tokens import scope, tokens
from django.contrib import messages 
from django.conf import settings
from django.core.paginator import Paginator
from django.forms import Form
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import api_view

from .models import AssignedTest, AnswerTest, Question, Answer, UserProfile
from .forms import FormAssignTest
from .email import sendEmail, sendEmailAnswer
from .errors import MyException, notValid, notCopleted, notSaved, toLate, done, sendError

# HOME ______________________________________________________________________________________________________
def home(request):
  return render(request, 'index.html')

# QUERY ____________________________________________________________________________________________________
@api_view(['GET', 'POST'])
def query(request, id='1'):
  if request.method == 'POST':
    form = Form(request.POST)
    if form.is_valid():
      # convert the answer
      item = {}
      answer=[]
      answers= {}
      for i in request.POST:
        if i != 'csrfmiddlewaretoken':
          item['question'] = int(i)
          item['choose'] = int(request.POST[i])
          answer.append(item)
          item = {}
      answers["answers"] = answer
      try:
        assigned = AssignedTest.objects.get(id=id)
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
      return render(request, 'save.html')
  # for GET method ******************
  else: 
    token = request.GET['token']
    validate = tokens.validate(token, scope=(), key=settings.SECRET_KEY, salt=settings.TOKEN_SALT, max_age=None)
    if validate:
      request.session['_query_id'] = id
      return redirect( 'quiz') # for nice url, without token
    else:
      raise Http404
  return render(request, 'query.html', {'psihotest': None, 'id': id})

  # QUIZ ____________________________________________________________________________________________________
def quiz(request):
  if ('_query_id' in request.session):
    id = request.session['_query_id']
    try:
      assigned = get_object_or_404(AssignedTest, id=id)
      # check if the test is in time
      if(assigned.data < datetime.date.today()):
        toLate() 
      # check if the test is completed or not
      elif (len(assigned.answer.all()) > 0):
        done() 
    except  Exception as e:
          messages.info(request, e)
  else:
      raise Http404
  return render(request, 'query.html', {'psihotest': assigned.psihotest, 'id': id})


# ASSIGN ____________________________________________________________________________________________________
@api_view(['GET', 'POST'])
def asign(request, id=-1):
  if request.method == 'POST':
    if (int(id) < 1):
      asignTest = AssignedTest()
    else:
      asignTest = get_object_or_404(AssignedTest, id=id)
    form = FormAssignTest(request.POST, instance=asignTest)
    # check whether it's valid:
    if form.is_valid():
      try:
        form.save()
        # add test to user
        user = UserProfile.objects.get(user = request.user)
        user.user_assign.add(asignTest)
        if (asignTest.id):
          sendEmail(request, 'Atribuire test', asignTest) 
        else:
          notSaved()
      except Exception as e:
        sendError(e)
      return render(request, 'save.html')
    else:
      notValid()
  # if is GET
  else:
    form = FormAssignTest()
    title = 'Atribuie test!'
    # Assign the choices based on User
    form.fields['psihotest'].queryset = UserProfile.objects.get(user = request.user).user_test.all()
    form.fields['data'].initial = datetime.date.today() + datetime.timedelta(days=14) # The default expire date will be 14 days from now
  return render(request, 'asign.html', {'form': form, 'title': title})


# ASSIGNED ____________________________________________________________________________________________________
@api_view(['GET', 'POST'])
def asigned(request):
  if request.method == 'POST':
    text_option = ['Nu ai selectat nici o actiune', 'Vezi test', 'Trimite rezultat pe e-mail', 'Retrimite e-mail', 'Modifica', 'Sterge',]
    if ('assign' in request.POST and (int(request.POST['option']) > 0)):
      if (int(request.POST['assign']) > 0):
        assigned = []
        assigned.append( AssignedTest.objects.get(id=request.POST['assign']) )
        selected = get_object_or_404(AssignedTest, id=request.POST['assign'])
        if (request.POST['option'] == '1'):
          answer = selected.answer.all()
          if (answer.count() > 0):
            text = ''
            total = 0
            for item in answer:
                total += int(item.choose.score)
            return render(request, 'view-result.html', {'answers': answer, 'total': total})
          else:
            text = 'Testul nu este completat! Nu are rezultate pentru a fi vizualizate!!!'
        elif (request.POST['option'] == '2'):
          if (selected.answer.count() > 0):
            email = request.user.email
            sendEmailAnswer(request, selected, email)
            text = f"Rezultat trimis cu succes pe e-mail-ul: {email}"
          else:
            text = 'Testul nu este completat! Nu are rezultate!!!'
        elif (request.POST['option'] == '3'):
           base = "{0}://{1}".format(request.scheme, request.get_host())
           sendEmail(request, 'Nu uita, ai un test atribuit', selected.email, f"{base}/query/{selected.id}" , selected.data, selected.message)
           text = f"Email trimis pentru {selected.name}, la adresa {selected.email}"
        elif (request.POST['option'] == '4'):
          form = FormAssignTest(instance=selected)
          title = 'Modifica atribuire test!'
          return render(request, 'asign.html', {'form': form, 'title': title, 'id': request.POST['assign']})
        elif (request.POST['option'] == '5'):
          return render(request, 'asigned-delete.html', { 'assigned': assigned[0], 'id': int(request.POST['assign'])})
    else:
      if (int(request.POST['option']) > 0):
        text = f"Nu ai selectat testul pentru care doresti actiunea: {text_option[int(request.POST['option'])]}"
      elif('assign' in request.POST):
        text = f"{text_option[int(request.POST['option'])]} pentru ID: {request.POST['assign']}"
      else:
        text = 'Nu ai selectat nimic!'
            
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


# DELETE - Assign ____________________________________________________________________________________________________
@api_view(['POST'])
def asigned_delete(request):
  remove = get_object_or_404(AssignedTest, id=request.POST['id'])
  remove.delete()
  return redirect('asigned')


# CONTACT ____________________________________________________________________________________________________
def about(request):
  return render(request, 'about.html')