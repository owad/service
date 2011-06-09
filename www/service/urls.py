from django.conf.urls.defaults import url, patterns
from www.service.views import ProductListView, ProductAddView, ProductDetailView, ClientEditView, ClientListView, ClientAddView, ClientDetailView, ReportView, html_pdf_preview, get_pdf
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('www.service.views',
    url(r'^$', login_required(ProductListView.as_view()), name='product-list'),
    url(r'^zgloszenia/$', login_required(ProductListView.as_view()), name='product-list'),
    url(r'^zgloszenia/(?P<status>\w+)/$', login_required(ProductListView.as_view()), name='product-list-by-status'),
    url(r'^zgloszenie/(?P<product_id>\d+)/$', login_required(ProductDetailView.as_view()), name='product-details'),
    url(r'^zgloszenie/podglad_wydruku/(?P<product_id>\d+)/$', 'html_pdf_preview', name='product-print-preview'),
    url(r'^zgloszenie/drukuj/(?P<product_id>\d+)/$', 'get_pdf', name='product-print'),
    url(r'^klienci/$', login_required(ClientListView.as_view()), name='client-list'),
    url(r'^klient/nowy/$', login_required(ClientAddView.as_view()), name='client-add'),
    url(r'^klient/(?P<client_id>\d+)/nowe_zgloszenie/$', login_required(ProductAddView.as_view()), name='product-add'),
    url(r'^klient/(?P<client_id>\d+)/$', login_required(ClientDetailView.as_view()), name='client-details'),
    url(r'^klient/edycja/(?P<client_id>\d+)/$', login_required(ClientEditView.as_view()), name='client-edit'),
    url(r'^raporty/$', login_required(ReportView.as_view()) , name='reports')
)