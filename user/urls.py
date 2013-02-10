from django.conf.urls.defaults import url, patterns
from django.contrib.auth.decorators import login_required

from user.views import UserEditView, UserListView, \
                    UserAddView, UserDetailView, UserAjaxSearch
from product.views import ProductAddView

urlpatterns = patterns('user.views',
    url(r'^$', login_required(UserListView.as_view()), name='user-list'),
    url(r'^nowy/$', login_required(UserAddView.as_view()), name='user-add'),
    url(r'^(?P<pk>\d+)/nowe_zgloszenie/$', login_required(ProductAddView.as_view()), name='product-add'),
    url(r'^(?P<pk>\d+)/$', login_required(UserDetailView.as_view()), name='user-details'),
    url(r'^edycja/(?P<pk>\d+)/$', login_required(UserEditView.as_view()), name='user-edit'),
    url(r'^szukaj/$', login_required(UserAjaxSearch.as_view()), name='user-search')
)

