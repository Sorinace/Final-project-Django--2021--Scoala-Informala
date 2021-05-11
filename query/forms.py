from django import forms

class AnswerSet(forms.Form):
  question = forms.CharField(label='question', max_length=100) 
  choose = forms.CharField(label='choose', max_length=100) 