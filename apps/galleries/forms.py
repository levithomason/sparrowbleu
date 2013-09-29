from django import forms
from apps.galleries.models import Gallery
    
class GalleryForm(forms.Form):
    name = forms.CharField(max_length=60)
    passcode = forms.CharField(max_length=60)
    number_of_images = forms.IntegerField()
    
class GalleryImageForm(forms.Form):
    image = forms.FileField()
    gallery = forms.ModelChoiceField(Gallery.objects.all())
