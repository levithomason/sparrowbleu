from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
   # Galleries
    url(r'^new-gallery/', 'apps.galleries.views.new_gallery', name='new_gallery'),
    url(r'^galleries/', 'apps.galleries.views.galleries', name='galleries'),
    url(r'^gallery/(?P<pk>\d+)/', 'apps.galleries.views.gallery_detail', name='gallery_detail'),

    # Gallery Images
    url(r'^new-gallery-image', 'apps.galleries.views.new_gallery_image', name='new_gallery_image'),
)