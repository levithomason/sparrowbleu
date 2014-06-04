import os
import re
import urllib
from django.db.models.signals import post_save, pre_delete
from django.db import models
from sorl.thumbnail import get_thumbnail, delete
from PIL import Image
from settings import *


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

    def total_images(self):
        return GalleryImage.objects.filter(gallery=self).count()

    def selected_images(self):
        return GalleryImage.objects.filter(gallery=self).filter(is_selected=True).count()

    def get_s3_directory_name(self):
        return '%s/' % self.pk


class GalleryImage(models.Model):
    gallery = models.ForeignKey('Gallery')
    is_selected = models.BooleanField(default=False)
    is_portrait = models.BooleanField()
    full_size_url = models.URLField(max_length=200, null=True)
    name = models.CharField(max_length=100, null=True)
    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)
    s3_object_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.full_size_url

    def _thumbnail(self, width, height):
        thumb_dimensions = '%sx%s' % (width, height)
        thumb = get_thumbnail(self.full_size_url, thumb_dimensions, quality=85, crop='noop', upscale=False, padding=True)
        url_no_args = re.sub(r'\?.*', '', thumb.url)
        return url_no_args

    def thumbnail(self):
        return self._thumbnail(720, 720)

    #def fullscreen(self):
        #return self._thumbnail(1200, 1200)

    def process(self):
        urllib.urlretrieve(self.full_size_url, filename=self.name)
        image_file = Image.open(self.name)

        self.width = image_file.size[0]
        self.height = image_file.size[1]
        self.is_portrait = image_file.size[0] < image_file.size[1]
        self.generate_thumbnails()
        self.save()

        os.remove('%s' % self.name)

    def generate_thumbnails(self):
        self.thumbnail()
        #self.fullscreen()

    def delete_image_files(self):
        # AWS S3 original image
        boto_bucket.delete_key(self.s3_object_name)

        # sorl thumbnail
        delete(self.full_size_url)


def process_gallery_image(sender, **kwargs):
    if kwargs['created']:
        gallery_image = kwargs['instance']
        gallery_image.process()


def delete_gallery_image_files(sender, **kwargs):
    gallery_image = kwargs['instance']
    gallery_image.delete_image_files()


post_save.connect(process_gallery_image, sender=GalleryImage)
pre_delete.connect(delete_gallery_image_files, sender=GalleryImage)
