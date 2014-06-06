from django.core.management.base import BaseCommand, CommandError
from apps.galleries.models import Gallery
from optparse import make_option


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--dimensions',
                    action='store_true',
                    dest='dimensions',
                    default=False,
                    help='Only update width, height, and is_portrait.'),
        make_option('--thumbnails',
                    action='store_true',
                    dest='thumbnails',
                    default=False,
                    help='Only generate thumbnails.'),
        make_option('--s3-object-names',
                    action='store_true',
                    dest='s3_object_names',
                    default=False,
                    help='Only update s3_object_name (from full_size_url).'),
    )

    args = '<gallery_id gallery_id ...>'
    help = 'Process gallery image meta data and/or thumbnails.  If no options are passed, all options are processed.'

    def handle(self, *args, **options):

        if len(args) == 0:
            galleries = Gallery.objects.all()

        else:
            galleries = []
            for gallery_id in args:
                try:
                    galleries.append(Gallery.objects.get(pk=int(gallery_id)))
                except Gallery.DoesNotExist:
                    raise CommandError('Gallery %s does not exist' % gallery_id)

        current_gallery = 1
        total_galleries = len(galleries)

        for gallery in galleries:
            self.stdout.write('\n    ----------------------------------------')
            self.stdout.write('    %s' % (gallery))
            self.stdout.write('    Gallery %s of %s' % (current_gallery, total_galleries))
            self.stdout.write('    ----------------------------------------')

            gallery_images = gallery.galleryimage_set.all()
            current_image = 1
            total_images = len(gallery_images)

            for gallery_image in gallery_images:
                self.stdout.write('\n    %s' % (gallery_image.name))
                self.stdout.write('    Image %s of %s' % (current_image, total_images))

                no_options_passed =\
                    not options['dimensions'] and\
                    not options['s3_object_names'] and\
                    not options['thumbnails']

                if options['dimensions'] or no_options_passed:
                    self.stdout.write('        - setting dimensions')
                    #gallery_image.set_dimensions()

                if options['s3_object_names'] or no_options_passed:
                    self.stdout.write('        - setting s3_object_name')
                    #object_name = gallery_image.set_s3_object_name()

                if options['thumbnails'] or no_options_passed:
                    self.stdout.write('        - making thumbnails')
                    #gallery_image.generate_thumbnails()

                self.stdout.write('        - done!')

                current_image += 1

            current_gallery += 1
