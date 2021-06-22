from rest_framework import viewsets

from .serializers import AssignedSerializers, PsihoTestSerializers, AnswerSerializers
from query.models import AssignedTest, PsihoTest, AnswerTest

class AnswerTestViewSets(viewsets.ModelViewSet):
    queryset = AnswerTest.objects.all()
    serializer_class = AnswerSerializers


class PsihoTestViewSets(viewsets.ModelViewSet):
    queryset = PsihoTest.objects.all()
    serializer_class = PsihoTestSerializers


class AssignViewSets(viewsets.ModelViewSet):
    queryset = AssignedTest.objects.all()
    serializer_class = AssignedSerializers

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(email__icontains=search)
        return qs
