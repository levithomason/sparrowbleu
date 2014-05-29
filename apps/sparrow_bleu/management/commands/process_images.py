from django.core.management.base import BaseCommand, CommandError
from apps.galleries.models import Gallery
from optparse import make_option


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--thumbs-only',
                    action='store_true',
                    dest='thumbs_only',
                    default=False,
                    help='Generate thumbnails only, skip meta data.'),
    )

    args = '<gallery_id gallery_id ...>'
    help = 'Process gallery image meta data and/or thumbnails'

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

        self.stdout.write('\nProcessing %s galleries...' % len(galleries))

        for gallery in galleries:
            self.stdout.write('\n    ----------------------------------------')
            self.stdout.write('    %s' % gallery)
            self.stdout.write('    ----------------------------------------')

            for gallery_image in gallery.galleryimage_set.all():
                self.stdout.write('\n    %s' % gallery_image.name)
                if options['thumbs_only']:
                    self.stdout.write('        - making thumbs')
                    gallery_image.generate_thumbnails()
                else:
                    self.stdout.write('        - processing')
                    gallery_image.process()
                self.stdout.write('        - done')
