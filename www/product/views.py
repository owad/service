from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.db.models import Count
from django import template
from django.template import loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import simplejson

from product.models import Product
from product.forms import ProductForm
from person.models import Client
from product.forms import CommentForm

register = template.Library()

class ProductDetailView(CreateView):
    template_name = 'product/details.html'
    queryset = Product.objects.all()
    success_url = 'product-details'
    
    def get_context_data(self, **kwargs):
        data = CreateView.get_context_data(self, **kwargs)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        data['product'] = product
        data['user'] = self.request.user
        data['comment_list'] = product.comment_set.all().order_by('id')
        data['comment_form'] = CommentForm(initial={'user': self.request.user, 'product': product})
        data['hardware_comment_form'] = CommentForm(initial={'user': self.request.user, 'product': product})
        return data
    
    def get_initial(self):
        init = CreateView.get_initial(self)
        init['product'] = self.get_context_data()['product']
        init['user'] = self.request.user
        return init
    
class ProductListView(ListView):
    context_object_name = "product_list"
    queryset = None
    template_name = 'product/list.html'
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

class ProductAddView(CreateView):
    template_name = 'product/add.html'
    queryset = Product.objects.all()
    form_class = ProductForm
    success_url = 'product-details'
    
    def get_form_kwargs(self):
        kwargs = CreateView.get_form_kwargs(self)
        kwargs['initial']['user'] = self.request.user
        kwargs['initial']['client'] = get_object_or_404(Client, pk=self.kwargs['pk'])
        return kwargs
    
    def get_success_url(self):
        return reverse(self.success_url, kwargs={'pk': self.get_object().id})
    
class CommentAddView(CreateView):
    template_name = "comment/add.html"
    form_class = CommentForm
    success_url = 'product-details'
    
    def get_context_data(self, **kwargs):
        context_data = CreateView.get_context_data(self, **kwargs)
        context_data['product_id'] = self.kwargs['product_id']
        return context_data
    
    def form_valid(self, form):
        form.save()
        json = simplejson.dumps({'success': True, 'data': ''})
        return HttpResponse(json)
    
    def form_invalid(self, form):
        html = loader.render_to_string(self.template_name, 
                                       dictionary=self.get_context_data(form=form), 
                                       context_instance=RequestContext(self.request))
        json = simplejson.dumps({'success': False, 'data': html})
        return HttpResponse(json)
    
    def get_success_url(self):
        return reverse(self.success_url, kwargs={'pk': self.kwargs['product_id']})
