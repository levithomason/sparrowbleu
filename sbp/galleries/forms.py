from django import forms

class GalleryForm(forms.Form):
    name = models.CharField(max_length=60)
    passcode = models.CharField(max_length=60)
    images = models.ImageField(upload_to="/where_is_this")