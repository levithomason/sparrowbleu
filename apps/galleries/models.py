from django.db.models.signals import post_save
from sorl.thumbnail import get_thumbnail
from django.db import models
import urllib
import os
from settings import MEDIA_ROOT
from PIL import Image

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
    is_portrait = models.BooleanField()
    full_size_url = models.URLField(max_length=200, null=True)
    large_thumb_url = models.URLField(max_length=200, null=True)
    small_thumb_url = models.URLField(max_length=200, null=True)
    name = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.full_size_url

    def small_thumb(self):
        if self.is_portrait:
            thumb = get_thumbnail(self.full_size_url, '270x360', quality=90, crop='center')
        else:
            thumb = get_thumbnail(self.full_size_url, '360x270', quality=90, crop='center')
        return thumb.url

    def medium_thumb(self):
        if self.is_portrait:
            thumb = get_thumbnail(self.full_size_url, '360x480', quality=90, crop='center')
        else:
            thumb = get_thumbnail(self.full_size_url, '480x360', quality=90, crop='center')
        return thumb.url

    def large_thumb(self):
        if self.is_portrait:
            thumb = get_thumbnail(self.full_size_url, '480x640', quality=90, crop='center')
        else:
            thumb = get_thumbnail(self.full_size_url, '640x480', quality=90, crop='center')
        return thumb.url


def make_thumbnails(sender, **kwargs):
    if kwargs['created']:
        gallery_image = kwargs['instance']

        file_name = os.path.join(MEDIA_ROOT, gallery_image.name)
        urllib.urlretrieve(gallery_image.full_size_url, filename=file_name)
        image_file = Image.open(file_name)
        image_size = image_file.size

        gallery_image.is_portrait = image_size[0] < image_size[1]

        gallery_image.small_thumb()
        gallery_image.medium_thumb()
        gallery_image.large_thumb()

post_save.connect(make_thumbnails, sender=GalleryImage)
