from datetime import date
from rest_framework import viewsets

from .serializers import AssignedSerializers, PsihoTestSerializers, AnswerSerializers
from query.models import AssignedTest, PsihoTest, AnswerTest
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class AnswerTestViewSets(viewsets.ModelViewSet):
    queryset = AnswerTest.objects.all()
    serializer_class = AnswerSerializers


class PsihoTestViewSets(viewsets.ModelViewSet):
    queryset = PsihoTest.objects.all()
    serializer_class = PsihoTestSerializers


class AssignViewSets(viewsets.ModelViewSet):
    queryset = AssignedTest.objects.all()
    serializer_class = AssignedSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        
        qs = qs.filter(data__gte=date.today()) # valid data, in time
        qs = qs.filter(answer__exact=None) # not completed
        if search:
            qs = qs.filter(email__iexact=search) # user e-mail
        return qs
