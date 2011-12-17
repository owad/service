from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q
from django.db.models import Sum
import datetime

from product.models import Product, Comment
from report.forms import ReportForm

class ReportView(FormView):
    template_name = 'reports/main.html'
    
    form_class = ReportForm
    _form = None
    _report_data = None
    _comments = None
    
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser: return super(ReportView, self).get(request, *args, **kwargs)
        else: return HttpResponseRedirect(reverse('product-list'))
    
    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        if self._form is None: self._form = ReportForm() 
        context['report_form'] = self._form
        if self._report_data:
            hard = self.get_report_sum('hardware')
            soft = self.get_report_sum('software')
            tran = self.get_report_sum('transport')
            summary = 0
            for cost in [hard, soft, tran]:
                if cost: summary += cost
            context['report'] = {}
            context['report']['hard'] = hard
            context['report']['soft'] = soft
            context['report']['tran'] = tran
            context['report']['sum'] = summary
        return context
    
    def post(self, request, *args, **kwargs):
        self._form = ReportForm(request.POST)
        if self._form.is_valid():
            self._report_data = self._form.data
        return self.get(request)
    
    def get_report_sum(self, cost_type):
        if self._report_data:
            startdate = datetime.date(year=int(self._report_data['start_date_year']), month=int(self._report_data['start_date_month']), day=int(self._report_data['start_date_day']))
            enddate = datetime.date(year=int(self._report_data['end_date_year']), month=int(self._report_data['end_date_month']), day=int(self._report_data['end_date_day']))
            products = Product.objects.filter( Q(created__gte=startdate) 
                                    & Q(created__lte=enddate)
                                    & Q(warranty__in=self._report_data.getlist('warranty'))
                                    & Q(user__in=self._report_data.getlist('user'))
                                   )
            data = Comment.objects.filter(product__in=products).aggregate(result=Sum(cost_type))
            return data['result']
        return 0
