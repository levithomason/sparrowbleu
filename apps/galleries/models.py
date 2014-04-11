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

    def get_desktop_url(self):
        return "/gallery/%s/%s" % ('d', self.passcode)

    def get_mobile_url(self):
        return "/gallery/%s/%s" % ('m', self.passcode)

    def selected_images(self):
        return GalleryImage.objects.filter(gallery=self).filter(is_selected=True).count()

    def get_s3_directory_name(self):
        s3_dir = '%s/' % self.pk

        return s3_dir


class GalleryImage(models.Model):
    gallery = models.ForeignKey('Gallery')
    is_selected = models.BooleanField(default=False)
    is_portrait = models.BooleanField()
    full_size_url = models.URLField(max_length=200, null=True)
    name = models.CharField(max_length=100, null=True)
    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return self.full_size_url

    def _thumbnail(self, width, height):
        thumb_dimensions = '%sx%s' % (width, height)
        thumb = get_thumbnail(self.full_size_url, thumb_dimensions, quality=80, crop='noop', upscale=False, padding=True)

        return thumb.url

    def thumbnail(self):
        return self._thumbnail(360, 360)

    def fullscreen(self):
        return self._thumbnail(1200, 1200)


def process_gallery_image(sender, **kwargs):
    if kwargs['created']:
        gallery_image = kwargs['instance']

        urllib.urlretrieve(gallery_image.full_size_url, filename=gallery_image.name)
        image_file = Image.open(gallery_image.name)

        gallery_image.width = image_file.size[0]
        gallery_image.height = image_file.size[1]
        gallery_image.is_portrait = image_file.size[0] < image_file.size[1]
        gallery_image.thumbnail()
        gallery_image.fullscreen()
        gallery_image.save()

        os.remove(gallery_image.name)


post_save.connect(process_gallery_image, sender=GalleryImage)
