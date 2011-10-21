from django.conf.urls.defaults import url, patterns
from django.contrib.auth.decorators import login_required

from product.views import ProductListView, ProductAddView, ProductDetailView, CommentAddView

urlpatterns = patterns('product.views',
    url(r'^$', login_required(ProductListView.as_view()), name='product-list'),
    url(r'^zgloszenia/$', login_required(ProductListView.as_view()), name='product-list'),
    url(r'^zgloszenia/(?P<status>\w+)/$', login_required(ProductListView.as_view()), name='product-list-by-status'),
    url(r'^zgloszenie/(?P<pk>\d+)/$', login_required(ProductDetailView.as_view()), name='product-details'),
    url(r'^klient/(?P<pk>\d+)/nowe_zgloszenie/$', login_required(ProductAddView.as_view()), name='product-add'),
    url(r'^zgloszenie/(?P<product_id>\d+)/nowy_komentarz/$', login_required(CommentAddView.as_view()), name='comment-add'),

)
