from django import forms
from apps.galleries.models import Gallery


class GalleryForm(forms.Form):
    name = forms.CharField(max_length=60)
    passcode = forms.CharField(max_length=60)
    number_of_images = forms.IntegerField(min_value=0)
    cost_per_extra_image = forms.IntegerField(min_value=0)


class GalleryImageForm(forms.Form):
    gallery = forms.ModelChoiceField(Gallery.objects.all())
    full_size_url = forms.URLField(max_length=200)
    name = forms.CharField(max_length=100)


class ClientAccessForm(forms.Form):
    passcode = forms.CharField(max_length=60)
