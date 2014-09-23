from __future__ import division
import os
import re
import urllib
from django.db.models.signals import post_save, pre_delete
from django.db import models
from PIL import Image
from sorl.thumbnail import get_thumbnail
import tasks


class Gallery(models.Model):
    name = models.CharField(max_length=60)
    passcode = models.CharField(max_length=60)
    number_of_images = models.PositiveIntegerField()
    cost_per_extra_image = models.PositiveIntegerField(default=20.00)

    def __unicode__(self):
        return self.name

    @property
    def selected_image_count(self):
        return self.galleryimage_set.filter(is_selected=True).count()

    @property
    def total_image_count(self):
        return self.galleryimage_set.count()

    def get_desktop_url(self):
        return "/gallery/%s/%s" % ('d', self.passcode)

    def get_mobile_url(self):
        return "/gallery/%s/%s" % ('m', self.passcode)

    def get_s3_directory_name(self):
        return '%s/' % self.pk


class GalleryImage(models.Model):
    full_size_url = models.URLField(max_length=200, null=True)
    gallery = models.ForeignKey('Gallery')
    height = models.PositiveIntegerField(null=True)
    is_portrait = models.BooleanField()
    is_selected = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=True)
    s3_object_name = models.CharField(max_length=200)
    width = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return self.full_size_url

    @property
    def _thumbnail_size(self):
        """
        The maximum thumbnail dimension.  Used for generating thumbnails.
        """
        return 720

    @property
    def _template_thumbnail_size(self):
        """
        This is used to calculate the size of the template_thumbnail_<width/height>.
        We use _thumbsize_size / 2 so the template renders the images at 2x.
        """
        return self._thumbnail_size / 2

    @property
    def template_thumbnail_width(self):
        """
        The width in pixels that the thumbnail should be rendered in the template.
        Accounts for portrait/landscape, maintains aspect ratio, and does not exceed _template_thumbnail_size.
        """
        max_thumb_width = self.width * (self._template_thumbnail_size / self.height)

        if self.is_portrait:
            if self.width >= self._template_thumbnail_size:
                return self._template_thumbnail_size
            else:
                return self.width

        else:
            if self.width < max_thumb_width:
                return self.width
            else:
                return max_thumb_width

    @property
    def template_thumbnail_height(self):
        """
        The height in pixels that the thumbnail should be rendered in the template.
        Accounts for portrait/landscape, maintains aspect ratio, and does not exceed _template_thumbnail_size.
        """
        max_thumb_height = self.height * (self._template_thumbnail_size / self.width)

        if self.is_portrait:
            if self.height < max_thumb_height:
                return self.height
            else:
                return max_thumb_height
        else:
            if self.height >= self._template_thumbnail_size:
                return self._template_thumbnail_size
            else:
                return self.height

    def _get_thumbnail(self, width, height):
        """
        Wrapper for sorl thumbnail's get_thumbnail.  Used for creating various image thumbnails.
        Returns a thumbnail url without arguments, such as an S3 Signature.
        """
        dimensions = '%sx%s' % (width, height)
        thumb = get_thumbnail(self.full_size_url, dimensions, quality=85, crop='noop', upscale=False, padding=True)
        url_no_args = re.sub(r'\?.*', '', thumb.url)
        return url_no_args

    #def fullscreen(self):
        #return self._get_thumbnail(1200, 1200)

    def generate_thumbnails(self):
        """
        Generates image thumbnails
        """
        self.thumbnail()
        #self.fullscreen()

    def process(self):
        """
        Sets image dimensions, s3_object_name, and generates thumbnails in one run
        """
        self.set_dimensions()
        self.set_s3_object_name()
        self.generate_thumbnails()

    def set_dimensions(self):
        """
        Sets image width, height, and is_portrait
        """
        urllib.urlretrieve(self.full_size_url, filename=self.name)
        image_file = Image.open(self.name)
        width = image_file.size[0]
        height = image_file.size[1]
        is_portrait = image_file.size[0] < image_file.size[1]
        os.remove('%s' % self.name)

        self.width = width
        self.height = height
        self.is_portrait = is_portrait
        self.save()

    def set_s3_object_name(self):
        """
        Sets s3_object_name
        """
        self.s3_object_name = re.sub(r'http.*com\/', '', '%s' % self.full_size_url)
        self.save()

    def thumbnail(self):
        """
        Returns the thumbnail for the image.
        """
        return self._get_thumbnail(self._thumbnail_size, self._thumbnail_size)


def process_gallery_image(sender, **kwargs):
    if kwargs['created']:
        gallery_image = kwargs['instance']
        gallery_image.process()


def delete_gallery_images(sender, **kwargs):
    gallery = kwargs['instance']

    print '################'
    print gallery
    print '#'
    print gallery.pk
    print '################'

    tasks.delete_gallery_images.delay(gallery.pk)


pre_delete.connect(delete_gallery_images, sender=Gallery)
post_save.connect(process_gallery_image, sender=GalleryImage)
