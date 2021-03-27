from django import forms

class NameForm(forms.Form):
    your_id = forms.CharField(label='Your id id', max_length=8)
    your_pw = forms.CharField(label='Your pw pw', max_length=20)