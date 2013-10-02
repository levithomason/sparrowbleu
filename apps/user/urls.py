from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^user_login', 'apps.user.views.user_login', name='user_login'),
    url(r'^user_logout', 'apps.user.views.user_logout', name='user_logout'),
)