from django.conf.urls.defaults import url, patterns
from django.contrib.auth.decorators import login_required

from person.views import ClientEditView, ClientListView, \
                    ClientAddView, ClientDetailView
from product.views import ProductAddView

urlpatterns = patterns('person.views',
    url(r'^klienci/$', login_required(ClientListView.as_view()), name='client-list'),
    url(r'^klient/nowy/$', login_required(ClientAddView.as_view()), name='client-add'),
    url(r'^klient/(?P<pk>\d+)/nowe_zgloszenie/$', login_required(ProductAddView.as_view()), name='product-add'),
    url(r'^klient/(?P<pk>\d+)/$', login_required(ClientDetailView.as_view()), name='client-details'),
    url(r'^klient/edycja/(?P<pk>\d+)/$', login_required(ClientEditView.as_view()), name='client-edit'),
)
