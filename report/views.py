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
        return Product.objects.get_for_report(self.request.GET)

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
