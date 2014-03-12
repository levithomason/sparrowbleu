from django.contrib import admin
from django.db import models


class Gallery(models.Model):
    name = models.CharField(max_length=60)
    passcode = models.CharField(max_length=60)
    number_of_images = models.PositiveIntegerField()
    cost_per_extra_image = models.PositiveIntegerField(default=20.00)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/gallery/%i/%s" % (self.id, self.passcode)

    def selected_images(self):
        return GalleryImage.objects.filter(gallery=self).filter(is_selected=True).count()

    def get_s3_directory_name(self):
        s3_dir = '%s/' % self.pk

        return s3_dir


class GalleryImage(models.Model):
    gallery = models.ForeignKey('Gallery')
    is_preview_image = models.BooleanField(default=False)
    is_selected = models.BooleanField(default=False)
    full_size_url = models.URLField(max_length=200, null=True)
    large_thumb_url = models.URLField(max_length=200, null=True)
    small_thumb_url = models.URLField(max_length=200, null=True)

    def __unicode__(self):
        return self.full_size_url

    admin.site.register(Gallery)
