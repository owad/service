from django.conf.urls.defaults import url, patterns
from www.report.views import ReportView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('report.views',
    url(r'^raporty/$', login_required(ReportView.as_view()) , name='reports'),
)