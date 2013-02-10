from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^zaloguj/$', login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^wyloguj/$', logout, {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profil/', include('account.urls')),
    url(r'^klient/', include('user.urls')),
    url(r'^pdf/', include('pdf.urls')),
    url(r'^raporty/', include('report.urls')),
    url(r'^', include('product.urls')),
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
        (r'^static_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

