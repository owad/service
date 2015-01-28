from django.conf.urls.defaults import url, patterns
from django.contrib.auth.decorators import login_required
from pdf.views import get_pdf

urlpatterns = patterns('pdf.views',
    url(r'^zgloszenie/drukuj/(?P<product_id>\d+)/$', 'get_pdf', name='product-print'),
)
