from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from galleries.views import Galleries


urlpatterns = patterns('',
    url(r'^$', 'sbp.views.Home', name='Home'),
    url(r'^client-access', 'sbp.views.ClientAccess', name='ClientAccess'),

    url(r'^new-gallery', 'sbp.galleries.views.NewGallery', name='NewGallery'),
    url(r'^gallery-posted', 'sbp.galleries.views.GalleryPosted', name='GalleryPosted'),
    url(r'^galleries', Galleries.as_view()),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
