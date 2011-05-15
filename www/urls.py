from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from www import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^zaloguj/$', login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^wyloguj/$', logout, {'template_name': 'registration/logout.html'}, name='logout'),
    (r'^admin/', include(admin.site.urls)),
    url(r'^profil/', include('www.account.urls')),
    url(r'^', include('www.service.urls')),
)
urlpatterns += staticfiles_urlpatterns()

#if settings.DEBUG:
#    urlpatterns += patterns('django.views.static',
#    (r'^static_media/(?P<path>.*)$', 
#        'serve', {
#        'document_root': '/srv/www/demo/www/static_media',
#        'show_indexes': True }),)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static__media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
