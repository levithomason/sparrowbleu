from django import forms
from apps.galleries.models import Gallery
    
class loginForm(forms.Form):
    username = forms.CharField(max_length=60)
    password = forms.CharField(max_length=60)
