from query.models import PsihoTest
from django import forms
import datetime
    
class AssignPsihoTest(forms.Form):
    tests = []
    # incarc denumirea testelor
    psTests = PsihoTest.objects.all()
    for item in psTests:
        tests.append(item.text)
    
    psihotest = forms.ChoiceField(label='Se atribuie testul', choices=tuple([(name, name) for name in tests]))
    name = forms.CharField(label='Pentru', max_length=100) 
    email = forms.EmailField(label='Cu adresa de e-mail') 
    # data dupa care testul nu mai poate fi accesat, security reason!
    data = forms.DateField(label='E valabil pana la data', initial=(datetime.date.today() + datetime.timedelta(days=14)), widget=forms.SelectDateWidget) 
    message = forms.CharField(label='Mesaj (opt.)', max_length=255, required=False)