# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, ListView, DetailView, View
from django.shortcuts import render_to_response, get_object_or_404, render
from www.service.models import Product, Client, Comment
from django.contrib.auth.models import User
from www.service.forms import CommentForm, ProductForm, ClientForm, ReportForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q, Count
import datetime
from django.db.models import Sum
from django import template
from django.template.loader import render_to_string
from django.template.context import RequestContext
import ho.pisa as pisa
import cStringIO as StringIO
import cgi

register = template.Library()

class ProductDetailView(DetailView):
    template_name = "service/product/details.html"
    _item = None
    _form = None
    
    def post(self, request, **kwargs):
        product = self.get_object()
        comment_form = CommentForm(request.POST)
        self._form = comment_form
        if comment_form.is_valid():
            comment_form.save()
            return HttpResponseRedirect(reverse('product-details', kwargs={'product_id': self.kwargs['product_id']}))
        if 'status_change' in request.POST:
            print product.status
            if product.status == Product.PROCESSING and 'set_courier' not in request.POST: product.status = Product.READY
            else: product.status = product.get_next_status()
            if 'parcel_number' in request.POST: product.parcel_number = request.POST['parcel_number']
            product.save()
            status_change_note = 'Status zmieniony na "%s"' % (product.get_status_name(),)
            comment = Comment(note=status_change_note, type=Comment.STATUS_CHANGE, user_id=self.request.user.id, product=product)
            comment.save()
            return HttpResponseRedirect(reverse('product-details', kwargs={'product_id': self.kwargs['product_id']}))
        return self.get(request)
    
    def get_object(self):
        self._item = get_object_or_404(Product, pk=self.kwargs['product_id'])
        return self._item
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['client'] = get_object_or_404(Client, pk=self._item.client_id)
        context['comment_list'] = self._item.comment_set.all().order_by('id')
        if not self._form: self._form = CommentForm(initial={'type': 'komentarz', 'product': self.kwargs['product_id'], 'user': self.request.user.id})
        context['comment_form'] = self._form
        return context
    
class ProductListView(ListView):
    context_object_name = "product_list"
    queryset = None
    template_name = "service/product/list.html"
    paginate_by = 50
    
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        count_result = Product.objects.values('status').annotate(count=Count('status'))
        tpl_status_counts = {}
        external = 0
        all = 0
        for row in count_result:
            tpl_status_counts[row['status']] = row['count']
            if row['status'] in (Product.EXTERNAL, Product.COURIER): 
                external = external + int(row['count'])
            all = all + int(row['count'])
        tpl_status_counts['wszystkie'] = all
        tpl_status_counts['serwis_zew'] = external
        context['counts'] = tpl_status_counts
        return context
    
    def get_queryset(self):
        q = self.get_search_query()
        if q:
            return Product.objects.filter(Q(id__icontains=q)|
                                          Q(name__icontains=q)|
                                          Q(producent__icontains=q)|
                                          Q(serial__icontains=q)|
                                          Q(parcel_number__icontains=q))
        else:
            if 'status' in self.kwargs and self.kwargs['status'] in Product.STATUSES:
                return Product.objects.all().filter(status__exact=self.kwargs['status'])
            else: return Product.objects.all()
    
    def get_search_query(self):
        q = None
        if 'q' in self.request.GET and self.request.GET['q']:
            q = self.request.GET['q'].strip()
        return q
    
class ProductAddView(TemplateView):
    template_name = "service/product/add.html"
    _form = None
    
    def get_context_data(self, **kwargs):
        context = super(ProductAddView, self).get_context_data(**kwargs)
        if not self._form: self._form = ProductForm(initial={'client': self.kwargs['client_id'], 'user': self.request.user.id})
        context['product_form'] = self._form
        context['client'] = get_object_or_404(Client, pk=self.kwargs['client_id'])
        return context
    
    def post(self, request, *args, **kwargs):
        self._form = ProductForm(request.POST)
        if self._form.is_valid():
            saved_instance = self._form.save()
            return HttpResponseRedirect(reverse('product-details', kwargs={'product_id': saved_instance.id}))
        return self.get(request)
    
class ClientListView(ListView):
    context_object_name = "client_list"
    queryset = None
    template_name = "service/client/list.html"
    paginate_by = 50
    
    def get_queryset(self):
        q = self.get_search_query()
        if q:
            return Client.objects.filter(Q(id__icontains=q)|
                                         Q(email__icontains=q)|
                                         Q(first_name__icontains=q)|
                                         Q(last_name__icontains=q)|
                                         Q(company_name__icontains=q)|
                                         Q(city__icontains=q)|
                                         Q(phone_number__icontains=q))
        else:
            return Client.objects.all()
    
    def get_search_query(self):
        q = None
        if 'q' in self.request.GET and self.request.GET['q']:
            q = self.request.GET['q'].strip()
        return q
    
class ClientAddView(TemplateView):
    template_name = "service/client/add.html"
    _form = None
    def get_context_data(self, **kwargs):
        context = super(ClientAddView, self).get_context_data(**kwargs)
        if not self._form: self._form = ClientForm()
        context['client_form'] = self._form
        return context
    def post(self, request, *args, **kwargs):
        self._form = ClientForm(request.POST)
        if self._form.is_valid():
            saved_instance = self._form.save()
            return HttpResponseRedirect(reverse('client-details', kwargs={'client_id': saved_instance.id}))
        return self.get(request)
class ClientDetailView(ProductListView):
    template_name = "service/client/details.html"
    
    def get_queryset(self):
        client = get_object_or_404(Client, pk=self.kwargs['client_id'])
        return client.product_set.all()
    
    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        client = get_object_or_404(Client, pk=self.kwargs['client_id'])
        context['client'] = client
        return context
        
class ReportView(TemplateView):
    template_name = 'service/reports/main.html'
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
            sum = 0
            for cost in [hard, soft, tran]:
                if cost: sum = sum + cost
            context['report'] = {}
            context['report']['hard'] = hard
            context['report']['soft'] = soft
            context['report']['tran'] = tran
            context['report']['sum'] = sum
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
    
def html_pdf_preview(request, product_id, as_pdf=False):
    product = get_object_or_404(Product, pk=product_id)
    data = {'product': product, 'client': product.client, 'comment_list': product.comment_set.all()}
    if as_pdf:
        return data
    return render_to_response('service/product/print2.html', data, RequestContext(request))
    
def get_pdf(request, product_id):
    data = html_pdf_preview(request, product_id, as_pdf = True)
    file_data = render_to_string('service/product/print2.html', data, RequestContext(request))
    myfile = StringIO.StringIO()
    pisa.CreatePDF(file_data.encode('UTF-8'), myfile, encoding='UTF-8')
    myfile.seek(0)
    response =  HttpResponse(myfile, mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=zgloszenie_nr_%s.pdf' % (data['product'].id,)
    return response
