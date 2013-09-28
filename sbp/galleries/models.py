from django.db import models
from django.forms import ModelForm


class Gallery(models.Model):
    name = models.CharField(max_length=60)
    passcode = models.CharField(max_length=60)
    
    def __unicode__(self):
        return self.name
    
class Image(models.Model):
    image = models.ImageField(upload_to="/")
    gallery = models.ForeignKey(Gallery)
    
    def __unicode__(self):
        return self.image
    
class GalleryForm(ModelForm):
    class Meta:
        model = Gallery
        fields = ['name', 'passcode']