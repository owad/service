from django.conf.urls.defaults import *
from account.views import Profile

urlpatterns = patterns('account.views',
    url(r'^$', Profile.as_view(), name='profile'),
)
