from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings

urlpatterns = patterns('',
    url(r'^$', 'apps.sparrow_bleu.views.home', name='Home'),
    url(r'^client-access/', 'apps.sparrow_bleu.views.client_access', name='client_access'),
    url(r'^login', 'apps.sparrow_bleu.views.user_login', name='user_login'),
    url(r'^logout', 'apps.sparrow_bleu.views.user_logout', name='user_logout'),

    url(r'^', include('apps.galleries.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),