from typing import Sequence
from django import forms
from .models import AssignedTest
from django.forms import ModelForm, widgets
import datetime

class FormAssignTest(ModelForm):
    class Meta:
        model = AssignedTest
        fields = ['psihotest', 'name', 'email', 'data', 'message']
        labels = {
            "psihotest": "Se atribuie testul",
            "name": "Pentru",
            "email": "Cu adresa de e-mail",
            "data": "E valabil pana la data",
            "message": "Mesaj (opt.)",
        }
        widgets = {
            "data": forms.SelectDateWidget
        }

    
# class AssignPsihoTest(forms.Form):

#     psihotest = forms.ModelChoiceField(label='Se atribuie testul', queryset=PsihoTest.objects.all() , empty_label=" -- Selecteaza un test --")
#     name = forms.CharField(label='Pentru', max_length=100) 
#     email = forms.EmailField(label='Cu adresa de e-mail') 
#     # data dupa care testul nu mai poate fi accesat, de obicei 14 zile de la atribuire, security reason!
#     data = forms.DateField(label='E valabil pana la data', initial=(datetime.date.today() + datetime.timedelta(days=14)), widget=forms.SelectDateWidget) 
#     message = forms.CharField(label='Mesaj (opt.)', max_length=255, required=False)
