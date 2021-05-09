from django.urls import path
from . import views

urlpatterns = [ 
  path('', views.home, name = 'home'), 
  path('query/', views.query, name = 'query'), 
  path('query/<str:id>', views.query, name = 'query_id'), 
  path('answer/', views.answer, name = 'answer'), 
  path('about/', views.about, name = 'about'),
  ]