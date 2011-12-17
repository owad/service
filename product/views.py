from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
from django import template
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.db.models import Q

from product.models import Product, Comment, Courier, File
from product.forms import ProductForm, CommentForm, StaffCommentForm, CourierCommentForm, FileForm
from person.models import Client

from datetime import datetime, timedelta

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
        if product.courier:
            data['courier'] = Courier.objects.get(pk=product.courier)
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
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        products = Product()
        context['counts'] = products.get_counts()
        return context
    
    def get_queryset(self):
        q = self.get_search_query()
        if q:
            if q.isdigit():
                return Product.objects.filter(id=q)
            else:
                return Product.objects.filter(Q(name__icontains=q)|
                                              Q(producent__icontains=q)|
                                              Q(serial__icontains=q)|
                                              Q(parcel_number__icontains=q)).filter(status__in=Product.IN_PROGRESS)
        else:
            if 'status' in self.kwargs:
                if self.kwargs['status'] == 'moje':
                    product_ids = Comment.objects.filter(user=self.request.user, status__in=Product.IN_PROGRESS, type=Comment.STATUS_CHANGE).values_list('product_id', flat=True)
                    return Product.objects.filter(id__in=product_ids)
                elif self.kwargs['status'] == 'przeterminowane':
                    return Product.objects.filter(Q(updated__lte=datetime.now() - timedelta(days=7),
                                                    status__in=(Product.NEW, Product.PROCESSING, Product.COURIER, Product.READY))|
                                                  Q(updated__lte=datetime.now() - timedelta(days=10),
                                                    status=Product.EXTERNAL))
                elif self.kwargs['status'] == 'moje_przeterminowane':
                    product_ids = Comment.objects.filter(user=self.request.user, status__in=Product.IN_PROGRESS, type=Comment.STATUS_CHANGE).values_list('product_id', flat=True)
                    return Product.objects.filter(id__in=product_ids).\
                                                  filter(Q(updated__lte=datetime.now() - timedelta(days=7),
                                                    status__in=(Product.NEW, Product.PROCESSING, Product.COURIER, Product.READY))|
                                                  Q(updated__lte=datetime.now() - timedelta(days=10),
                                                    status=Product.EXTERNAL))
                elif self.kwargs['status'] in Product.STATUSES:
                    return Product.objects.all().filter(status__exact=self.kwargs['status'])
            else:
                return Product.objects.all()
    
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
    new_id = None
    
    def get_context_data(self, **kwargs):
        context_data = CreateView.get_context_data(self, **kwargs)
        context_data['client'] = get_object_or_404(Client, pk=self.kwargs['pk'])
        return context_data
    
    def get_form_kwargs(self):
        kwargs = CreateView.get_form_kwargs(self)
        kwargs['initial']['user'] = self.request.user
        kwargs['initial']['client'] = get_object_or_404(Client, pk=self.kwargs['pk'])
        return kwargs
    
    def get_success_url(self):
        return reverse(self.success_url, kwargs={'pk': self.object.id})
    
class CommentAddView(CreateView):
    template_name = "comment/add.html"
    form_class = CommentForm
    success_url = 'product-details'
    
    def get_form_kwargs(self):
        kwargs = CreateView.get_form_kwargs(self)
        kwargs['initial']['user'] = self.request.user
        kwargs['initial']['product'] = get_object_or_404(Product, pk=self.kwargs['product_id'])
        return kwargs
    
    def get_context_data(self, **kwargs):
        context_data = CreateView.get_context_data(self, **kwargs)
        context_data['product'] = get_object_or_404(Product, pk=self.kwargs['product_id'])
        return context_data
    
    def get_form(self, form_class):
        product = self.get_context_data()['product']
        if product.status == Product.COURIER:
            form_class = CourierCommentForm
        elif self.request.user.is_staff:
            form_class = StaffCommentForm
        else:
            form_class = CommentForm
        return CreateView.get_form(self, form_class)
    
    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.request.POST['product'])
        new_comment = form.save(commit=False)
        save = True
        if 'status_change' in self.request.POST and int(self.request.POST['status_change']) > 0:
            new_status = product.set_next_status(self.request)
            new_comment.status = new_status
            if new_status == Product.LAST_STATUS and not self.request.user.is_staff:
                save = False
            if new_status == Product.READY:
                product.fixed_by = self.request.user.id
            new_comment.set_comment_type(int(self.request.POST['status_change']))
        json = simplejson.dumps({'success': True, 'data': ''})
        if save: 
            product.save()
            new_comment.status = product.status
            new_comment.save()
        return HttpResponse(json)
    
    def form_invalid(self, form):
        html = loader.render_to_string(self.template_name, 
                                       dictionary=self.get_context_data(form=form), 
                                       context_instance=RequestContext(self.request))
        json = simplejson.dumps({'success': False, 'data': html})
        return HttpResponse(json)
    
    def get_success_url(self):
        return reverse(self.success_url, kwargs={'pk': self.kwargs['product_id']})

class CommentDeleteView(DeleteView):
    template_name = "comment/delete.html"
    model = Comment
    success_url = 'product-details'
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        id = self.object.product.id
        if (request.user.is_staff and self.object.type == self.object.HARDWARE_ADD) or (request.user.is_superuser):
            self.object.delete()
        return HttpResponseRedirect(self.get_success_url(id))
    
    def get_template_names(self):
        return [self.template_view]
    
    def get_success_url(self, id):
        return reverse(self.success_url, kwargs={'pk': id})


class ProductFileAddView(CreateView):
    template_name = 'product/file_add.html'
    queryset = File.objects.all()
    form_class = FileForm
    success_url = 'product-details'
    
    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)
        context['product'] = get_object_or_404(Product, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        new_file = form.save(commit=False)
        if new_file.obj:
            new_file.product = self.get_context_data()['product']
            new_file.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse(self.success_url, kwargs={'pk': self.get_context_data()['product'].id})

def get_file(request, product_id, pk):
    f = get_object_or_404(File, pk=pk)
    if int(f.product.id) != int(product_id):
        return HttpResponseRedirect('/')
    response = HttpResponse(f.obj.read())
    response['Content-Disposition'] = 'attachment; filename=%s' % f.get_file_name()
    return response
    