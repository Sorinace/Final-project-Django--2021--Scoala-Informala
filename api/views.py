from datetime import date
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .serializers import AssignedSerializers, PsihoTestSerializers, AnswerSerializers
from query.models import AssignedTest, PsihoTest, AnswerTest
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class AnswerTestViewSets(viewsets.ModelViewSet):
    queryset = AnswerTest.objects.all()
    serializer_class = AnswerSerializers


class PsihoTestViewSets(viewsets.ModelViewSet):
    queryset = PsihoTest.objects.all()
    serializer_class = PsihoTestSerializers
    authentication_classes = []
    permission_classes =[IsAuthenticatedOrReadOnly]

class AssignViewSets(viewsets.ModelViewSet):
    queryset = AssignedTest.objects.all()
    serializer_class = AssignedSerializers
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes =[IsAuthenticatedOrReadOnly]

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