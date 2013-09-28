from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sbp.views.home', name='home'),
    url(r'^client-access', 'sbp.views.client_access', name='client_access'),
    url(r'^new-gallery', 'sbp.views.new_gallery', name='new_gallery'),
    
    url(r'^gallery-posted', 'sbp.galleries.views.gallery_posted', name='gallery_posted'),
    # url(r'^sbp/', include('sbp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
