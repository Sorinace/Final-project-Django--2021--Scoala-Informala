from django.urls import path
from . import views

urlpatterns = [ 
  path('', views.home, name = 'home'), 
  path('query/<str:id>', views.query, name = 'query'), 
  path('about/', views.about, name = 'about'),
  path('answer/', views.answer, name = 'answer'),
  path('asign/', views.asign, name = 'asign'),
  path('asigned/', views.asigned, name = 'asigned'),
  path('asigned/delete/', views.asigned_delete, name='asigned_delete'),
  ]