from django.contrib import admin
from django.db import models
from settings import MEDIA_ROOT

class Gallery(models.Model):
    name = models.CharField(max_length=60)
    passcode = models.CharField(max_length=60)
    number_of_images = models.PositiveIntegerField()
    
    def __unicode__(self):
        return self.name
     
    def get_absolute_url(self):
        return "/gallery/%i/" % self.id


class GalleryImage(models.Model):
    gallery = models.ForeignKey('Gallery')
    image = models.ImageField(upload_to=MEDIA_ROOT)
    
    def __unicode__(self):
        return self.image

admin.site.register(Gallery)