from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from galleries.views import galleries


urlpatterns = patterns('',
    url(r'^$', 'sbp.views.home', name='Home'),
    url(r'^client-access', 'sbp.views.client_access', name='client_access'),
    url(r'^login', 'sbp.views.user_login', name='user_login'),
    url(r'^logout', 'sbp.views.user_logout', name='user_logout'),

    url(r'^new-gallery', 'sbp.galleries.views.new_gallery', name='new_gallery'),
    url(r'^gallery-posted', 'sbp.galleries.views.gallery_posted', name='gallery_posted'),
    url(r'^galleries', galleries.as_view()),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
