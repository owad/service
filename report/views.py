from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from django.db.models import Q
from django.db.models import Sum

import datetime

from settings import PRODUCTS_PER_PAGE
from product.models import Product, Comment
from report.forms import ReportForm
from person.models import User


class ReportView(ListView):
    template_name = 'reports/main.html'
    form_class = ReportForm
    #paginate_by = PRODUCTS_PER_PAGE
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(ReportView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('product-list'))

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        if self.request.GET:
            form = self.form_class(data=self.request.GET)
        else:
            form = self.form_class()
            
        context['form'] = form
        
        if form.is_valid():
            context['report'] = self.get_report_sum()
        
        return context

    def get_queryset(self):
        get = self.request.GET
        if get:
            startdate = datetime.date(year=int(get['start_date_year']),
                                      month=int(get['start_date_month']),
                                      day=int(get['start_date_day']))
            enddate = datetime.date(year=int(get['end_date_year']),
                                    month=int(get['end_date_month']),
                                    day=int(get['end_date_day']))
            return Product.objects.filter(Q(created__gte=startdate)
                                          & Q(created__lte=enddate)
                                          & Q(warranty__in=get.getlist('warranty'))
                                          & Q(user__in=get.getlist('user')))
        return []

    def get_report_sum(self):
        if self.request.GET:
            data = Comment.objects.filter(product__in=self.get_queryset()).aggregate(soft=Sum('software'), hard=Sum('hardware'), tran=Sum('transport'))
            total = 0.00
            for key, value in data.items():
                total += float(value)
                data[key] = float(value)
            data['sum'] = total
            return data
        return None