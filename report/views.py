from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.db.models import Q
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime

from settings import PRODUCTS_PER_PAGE
from product.models import Product, Comment
from report.forms import ReportForm


class ReportView(ListView):
    template_name = 'reports/main.html'
    form_class = ReportForm
    # paginate_by = PRODUCTS_PER_PAGE

    @csrf_exempt
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
        queryset = Product.objects.get_closed()
        return self.apply_form_data(queryset)

    def apply_form_data(self, product_queryset):
        date_pattern = '%Y-%m-%d %H:%M:%S'
        get = self.request.GET
        if get:
            startdate = datetime.strptime('%s-%s-%s 00:00:00' % (get['start_date_year'], get['start_date_month'], get['start_date_day']), date_pattern)
            enddate = datetime.strptime('%s-%s-%s 23:59:59' % (get['end_date_year'], get['end_date_month'], get['end_date_day']), date_pattern)
            return product_queryset.filter(Q(created__gte=startdate) & Q(created__lte=enddate)
                                           & Q(warranty__in=get.getlist('warranty')) & Q(user__in=get.getlist('user')))
        return product_queryset

    def get_report_sum(self):
        if self.request.GET:
            data = Comment.objects.filter(product__in=self.get_queryset()).aggregate(soft=Sum('software'), hard=Sum('hardware'), tran=Sum('transport'))
            total = 0.00
            for key, value in data.items():
                val = float(value) if value is not None else 0.00
                data[key] = val
                total += val
            data['sum'] = total
            return data
        return None
