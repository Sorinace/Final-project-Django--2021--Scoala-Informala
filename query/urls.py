from django.urls import path
from . import views

urlpatterns = [ 
  path('', views.home, name = 'home'), 
  path('query/', views.query, name = 'query'), 
  path('about/', views.about, name = 'about'),
  path('answer/', views.answer, name = 'answer'),
  path('api/query/<str:id>', views.query_id, name = 'query_id'), 
  path('api/answer/', views.answer_api, name = 'answer_api'), 
  ]