from query.models import PsihoTest, UserProfile
from django import forms
import datetime
    
class AssignPsihoTest(forms.Form):
    tests = []
    # incarc doar denumirea testelor nu tot obiectul
    psTests = UserProfile.objects.all().values('user')
    for item in psTests:
        tests.append(item)
    
    psihotest = forms.ChoiceField(label='Se atribuie testul', choices=tuple([(name, name) for name in tests]))
    name = forms.CharField(label='Pentru', max_length=100) 
    email = forms.EmailField(label='Cu adresa de e-mail') 
    # data dupa care testul nu mai poate fi accesat, de obicei 14 zile de la atribuire, security reason!
    data = forms.DateField(label='E valabil pana la data', initial=(datetime.date.today() + datetime.timedelta(days=14)), widget=forms.SelectDateWidget) 
    message = forms.CharField(label='Mesaj (opt.)', max_length=255, required=False)