from rest_framework import viewsets

from .serializers import AssignedSerializers
from query.models import AssignedTest

class AssignViewSets(viewsets.ModelViewSet):
    queryset = AssignedTest.objects.all()
    serializer_class = AssignedSerializers

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(email__icontains=search)
        return qs
