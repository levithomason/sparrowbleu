from django.conf.urls import patterns, include, url
from django.contrib import admin

from apps.galleries.views import galleries

urlpatterns = patterns('',
    url(r'^$', 'apps.sparrow_bleu.views.home', name='Home'),
    url(r'^client-access', 'apps.sparrow_bleu.views.client_access', name='client_access'),
    url(r'^login', 'apps.sparrow_bleu.views.user_login', name='user_login'),
    url(r'^logout', 'apps.sparrow_bleu.views.user_logout', name='user_logout'),

    url(r'^new-gallery', 'apps.galleries.views.new_gallery', name='new_gallery'),
    url(r'^gallery-posted', 'apps.galleries.views.gallery_posted', name='gallery_posted'),
    url(r'^galleries', 'apps.galleries.views.galleries', name='galleries'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
