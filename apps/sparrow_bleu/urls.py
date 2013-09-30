from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'apps.sparrow_bleu.views.home', name='Home'),
    url(r'^client-access/', 'apps.sparrow_bleu.views.client_access', name='client_access'),
    url(r'^login', 'apps.sparrow_bleu.views.user_login', name='user_login'),
    url(r'^logout', 'apps.sparrow_bleu.views.user_logout', name='user_logout'),

    url(r'^', include('apps.galleries.urls')),
)
