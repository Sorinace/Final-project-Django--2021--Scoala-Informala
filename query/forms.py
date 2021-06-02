from query.models import PsihoTest, UserProfile
from django import forms
import datetime
    
class AssignPsihoTest(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields =('user_test', )
    
    psihotest = forms.ModelChoiceField(label='Se atribuie testul', queryset='user_test' , empty_label=" -- Selecteaza un test --")
    name = forms.CharField(label='Pentru', max_length=100) 
    email = forms.EmailField(label='Cu adresa de e-mail') 
    # data dupa care testul nu mai poate fi accesat, de obicei 14 zile de la atribuire, security reason!
    data = forms.DateField(label='E valabil pana la data', initial=(datetime.date.today() + datetime.timedelta(days=14)), widget=forms.SelectDateWidget) 
    message = forms.CharField(label='Mesaj (opt.)', max_length=255, required=False)

    def __init__(self, user, *args, **kwargs):
        super(AssignPsihoTest, self).__init__(*args, **kwargs)
        self.fields['user_test'].queryset = UserProfile.objects.filter(user=user)