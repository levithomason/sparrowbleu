from django.db import models
from django.forms import ModelForm


class Gallery(models.Model):
    name = models.CharField(max_length=60)
    passcode = models.CharField(max_length=60)
    images = models.ImageField(upload_to="/where_is_this")
    
    def __unicode__(self):
        return self.name
    
class GalleryForm(ModelForm):
    class Meta:
        model = Gallery