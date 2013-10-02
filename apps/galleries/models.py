import os

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
    image = models.ImageField(upload_to="gallery_images")
    is_preview_image = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.image.url

admin.site.register(Gallery)