# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.urlresolvers import reverse
from django.db.models import Q

from person.models import Client, User
from person.forms import ClientForm
from product.views import ProductListView

class ClientListView(ListView):
    context_object_name = "client_list"
    queryset = None
    template_name = "person/client/list.html"
    paginate_by = 50
    
    def get_queryset(self):
        q = self.get_search_query()
        if q:
            return Client.objects.filter(Q(first_name__icontains=q)|
                                         Q(last_name__icontains=q)|
                                         Q(company_name__icontains=q)|
                                         Q(phone_number__icontains=q))
        else:
            return Client.objects.all()
    
    def get_search_query(self):
        q = None
        if 'q' in self.request.GET and self.request.GET['q']:
            q = self.request.GET['q'].strip()
        return q
    
class ClientAddView(CreateView):
    template_name = "person/client/form.html"
    queryset = Client.objects.all()
    form_class = ClientForm
    success_url = 'client-details'
    
    def get_success_url(self):
        return reverse(self.success_url, kwargs={'pk': self.object.id})
    
class ClientEditView(UpdateView):
    template_name = "person/client/form.html"
    form_class = ClientForm
    queryset = Client.objects.all()
    
    def get_success_url(self):
        return reverse('client-details', kwargs={'pk': self.get_object().id})
    
class ClientDetailView(ProductListView):
    template_name = "person/client/details.html"
    
    def get_queryset(self):
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        return client.product_set.all()
    
    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        context['client'] = client
        return context
