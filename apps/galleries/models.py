import os
import urllib
from django.db.models.signals import post_save
from django.db import models
from sorl.thumbnail import get_thumbnail
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
    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return self.full_size_url

    def _thumbnail(self, size):
        w = self.width
        h = self.height
        if self.is_portrait:
            thumb_height = size
            thumb_width = int(round((size / float(h)) * float(w)))
        else:
            thumb_width = size
            thumb_height = int(round((size / float(w)) * float(h)))
        thumb_dimensions = '%sx%s' % (thumb_width, thumb_height)
        thumb = get_thumbnail(self.full_size_url, thumb_dimensions, quality=90, crop='center')
        return thumb.url

    def small_thumb(self):
        return self._thumbnail(360)

    def medium_thumb(self):
        return self._thumbnail(480)

    def large_thumb(self):
        return self._thumbnail(640)


def process_gallery_image(sender, **kwargs):
    if kwargs['created']:
        gallery_image = kwargs['instance']

        urllib.urlretrieve(gallery_image.full_size_url, filename=gallery_image.name)
        image_file = Image.open(gallery_image.name)

        gallery_image.width = image_file.size[0]
        gallery_image.height = image_file.size[1]
        gallery_image.is_portrait = image_file.size[0] < image_file.size[1]

        os.remove(gallery_image.name)

        gallery_image.small_thumb()
        gallery_image.medium_thumb()
        gallery_image.large_thumb()

post_save.connect(process_gallery_image, sender=GalleryImage)
