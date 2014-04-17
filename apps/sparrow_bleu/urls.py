from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings

urlpatterns = patterns('',
    url(r'^$', 'apps.sparrow_bleu.views.home', name='home'),

    url(r'^', include('apps.user.urls')),
    url(r'^', include('apps.galleries.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        # static files (images, css, javascript, etc.)
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

        # Uncomment the admin/doc line below to enable admin documentation:
        # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

        # Uncomment the next line to enable the admin:
        url(r'^admin/', include(admin.site.urls)),
    )
