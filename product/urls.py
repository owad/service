from django.conf.urls.defaults import url, patterns
from django.contrib.auth.decorators import login_required

from product.views import ProductListView, ProductAddView, ProductDetailView, CommentAddView,\
    CommentDeleteView, ProductFileAddView, get_file

urlpatterns = patterns('product.views',
    url(r'^$', login_required(ProductListView.as_view()), name='product-list'),
    url(r'^zgloszenia$', login_required(ProductListView.as_view()), name='product-list'),
    url(r'^zgloszenia/(?P<status>\w+)$', login_required(ProductListView.as_view()), name='product-list-by-status'),
    url(r'^zgloszenie/(?P<pk>\d+)$', login_required(ProductDetailView.as_view()), name='product-details'),
    url(r'^klient/(?P<pk>\d+)/nowe_zgloszenie$', login_required(ProductAddView.as_view()), name='product-add'),
    url(r'^zgloszenie/(?P<product_id>\d+)/nowy_komentarz$', login_required(CommentAddView.as_view()), name='comment-add'),
    url(r'^komenatrz/usun/(?P<pk>\d+)$', login_required(CommentDeleteView.as_view()), name='comment-del'),
    url(r'^zgloszenie/(?P<pk>\d+)/pliki/dodaj/$', login_required(ProductFileAddView.as_view()), name='product-file-add'),
    url(r'^zgloszenie/(?P<product_id>\d+)/plik/pobierz/(?P<pk>\d+)/$', login_required(get_file), name='product-get-file')
)
