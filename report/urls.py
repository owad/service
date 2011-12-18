from django.conf.urls.defaults import url, patterns
from report.views import ReportView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('report.views',
    url(r'^$', login_required(ReportView.as_view()) , name='reports'),
)
