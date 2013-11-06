from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
   # Galleries
    url(r'^new-gallery/', 'apps.galleries.views.new_gallery', name='new_gallery'),
    url(r'^galleries/', 'apps.galleries.views.galleries', name='galleries'),

    url(r'^gallery/(?P<pk>\d+)/(?P<passcode>\w)', 'apps.galleries.views.gallery_detail', name='gallery_detail'),
    url(r'^gallery/(?P<pk>\d+)', 'apps.galleries.views.gallery_detail', name='gallery_detail'),
    url(r'^gallery/', 'apps.galleries.views.gallery_detail', name='gallery_detail'),

    url(r'^gallery/(?P<gallery_pk>\d+)/(?P<passcode>\w)/select_image/(?P<image_pk>\w)',
        'apps.galleries.views.select_gallery_image', name='select_gallery_image'),

    url(r'^client-access/', 'apps.galleries.views.client_access', name='client_access'),

    # Gallery Images
    url(r'^new-gallery-image', 'apps.galleries.views.new_gallery_image', name='new_gallery_image'),
)

