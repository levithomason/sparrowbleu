from django.db import models

class Gallery(models.Model):
    name = models.CharField(max_length=60)
    passcode = models.CharField(max_length=60)
    number_of_images = models.PositiveIntegerField()
    
    def __unicode__(self):
        return self.name
    
class Image(models.Model):
    image = models.ImageField(upload_to="/")
    gallery = models.ForeignKey(Gallery)
    
    def __unicode__(self):
        return self.image