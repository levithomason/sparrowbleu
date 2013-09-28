from django import forms
from sbp.galleries.models import Gallery
    
class GalleryForm(forms.Form):
    name = forms.CharField(max_length=60)
    passcode = forms.CharField(max_length=60)
    number_of_images = forms.IntegerField()