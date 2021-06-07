from django import forms
from .models import AssignedTest
from django.forms import ModelForm

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

