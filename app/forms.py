from django import forms

class MyForm(forms.Form):
    start = forms.CharField(max_length=20)
    wait = forms.IntegerField()
    amount = forms.FloatField()
    base = forms.CharField(max_length=3)
    target = forms.CharField(max_length=3)
