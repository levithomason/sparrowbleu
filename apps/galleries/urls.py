from django.conf.urls import patterns, url

urlpatterns = patterns('',
   # Galleries
    url(r'^create-gallery/', 'apps.galleries.views.create_gallery', name='create_gallery'),
    url(r'^edit-gallery/(?P<pk>\d+)', 'apps.galleries.views.edit_gallery', name='edit_gallery'),
    url(r'^delete-gallery/', 'apps.galleries.views.delete_gallery', name='delete_gallery'),
    url(r'^galleries/', 'apps.galleries.views.galleries', name='galleries'),

    url(r'^gallery/(?P<pk>\d+)/(?P<passcode>\w)', 'apps.galleries.views.gallery_detail', name='gallery_detail'),
    url(r'^gallery/(?P<pk>\d+)', 'apps.galleries.views.gallery_detail', name='gallery_detail'),
    url(r'^gallery/', 'apps.galleries.views.gallery_detail', name='gallery_detail'),

    url(r'^send-completed-gallery/(?P<pk>\d+)', 'apps.galleries.views.send_completed_gallery', name='send_completed_gallery'),
    url(r'^gallery-completed-thanks/', 'apps.galleries.views.gallery_completed_thanks', name='gallery_completed_thanks'),

    url(r'^client-access/', 'apps.galleries.views.client_access', name='client_access'),

    # Gallery Images
    url(r'^create-gallery-image/', 'apps.galleries.views.create_gallery_image', name='create_gallery_image'),
    url(r'^s3-sign-upload/', 'apps.galleries.views.s3_sign_upload', name='s3_sign_upload'),
    url(r'^toggle-select-gallery-image/', 'apps.galleries.views.toggle_select_gallery_image', name='toggle_select_gallery_image'),
)
