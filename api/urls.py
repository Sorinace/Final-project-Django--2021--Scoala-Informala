from django.urls import path, include
from rest_framework import routers

from .views import AssignViewSets, PsihoTestViewSets, AnswerTestViewSets

router = routers.DefaultRouter()
router.register('assigned', AssignViewSets)
router.register('psiho_test', PsihoTestViewSets)
# router.register('answer_test', AnswerTestViewSets)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework'))
] 