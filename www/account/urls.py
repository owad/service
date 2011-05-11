from django.conf.urls.defaults import *
from account.views import *

urlpatterns = patterns('www.service.views',
    url(r'^$', Profile.as_view(), name='profile'),
)