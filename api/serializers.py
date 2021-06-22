from query.models import AssignedTest
from django.contrib.auth import models
from rest_framework import serializers

from query.models import AssignedTest

class AssignedSerializers(serializers.ModelSerializer):
    class Meta:
        model = AssignedTest
        fields = '__all__'