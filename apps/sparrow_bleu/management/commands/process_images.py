import os
import urllib
from django.core.management.base import NoArgsCommand
from apps.galleries.models import GalleryImage
from PIL import Image


class Command(NoArgsCommand):
    help = 'Process image thumbs and other meta data'

    def handle_noargs(self, **options):
        for gallery_image in GalleryImage.objects.all():
            print '%s' % gallery_image.name
            print '    - downloading'
            urllib.urlretrieve(gallery_image.full_size_url, filename=gallery_image.name)
            image_file = Image.open(gallery_image.name)

            gallery_image.width = image_file.size[0]
            gallery_image.height = image_file.size[1]
            print '    - dimensions: %s x %s' % (gallery_image.width, gallery_image.height)

            gallery_image.is_portrait = image_file.size[0] < image_file.size[1]
            print '    - is_portait: %s' % gallery_image.is_portrait

            print '    - ...making small thumb'
            gallery_image.thumbnail()

            print '    - ...making full thumb'
            gallery_image.fullscreen()

            print '    - ...saving'
            gallery_image.save()

            print '    - ...cleaning up'
            os.remove(gallery_image.name)

            print '    - done!\n'
