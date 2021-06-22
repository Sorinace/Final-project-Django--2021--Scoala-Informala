from django.urls import path, include
from rest_framework import routers

from .views import AssignViewSets

router = routers.DefaultRouter()
router.register('assigned', AssignViewSets)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework'))
] 