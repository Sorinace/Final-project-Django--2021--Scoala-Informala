from datetime import date
import re
from rest_framework import serializers, viewsets
from rest_framework import response
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .serializers import AssignedSerializers, PsihoTestSerializers, AnswerSerializers
from query.models import Answer, AssignedTest, PsihoTest, AnswerTest, Question, Question, Answer, User
from query.email import sendEmailAnswer

class AnswerTestViewSets(viewsets.ModelViewSet):
    queryset = AnswerTest.objects.all()
    serializer_class = AnswerSerializers
    permission_classes =[IsAuthenticated]

class PsihoTestViewSets(viewsets.ModelViewSet):
    queryset = PsihoTest.objects.all()
    serializer_class = PsihoTestSerializers
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes =[IsAuthenticated]

class AssignViewSets(viewsets.ModelViewSet):
    queryset = AssignedTest.objects.all()
    serializer_class = AssignedSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes =[IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
    
        qs = qs.filter(data__gte=date.today()) # valid data, in time
        qs = qs.filter(answer__exact=None) # not completed
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(email__iexact=search) # user e-mail
        return qs

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)

    def create(self, request):
        if True:
            if request.method == 'POST':
                data = request.data
                item={}
                answer=[]
                answers={}
                id = int(data['id'])
                # formating data received
                for ans in data['answer']:
                    item['question'] = int(ans)
                    item['choose'] = int(data['answer'][ans])
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
                        sendEmailAnswer(request, assigned, email, 'NA') 
                    else:
                        return Response(False)
                except:
                    return Response(False)

        return Response(True)