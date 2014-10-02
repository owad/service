# -*- coding: utf-8 -*-

from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.utils.encoding import smart_str
from django.template import loader, RequestContext

from person.models import Client
from person.forms import ClientForm
from product.views import ProductListView

from settings import CLIENTS_PER_PAGE


class ClientListView(ListView):
    context_object_name = "client_list"
    queryset = None
    template_name = "person/client/list.html"
    paginate_by = CLIENTS_PER_PAGE
    
    def get_queryset(self):
        q = self.get_search_query()
        if q:
            return Client.objects.filter(Q(first_name__icontains=q)|
                                         Q(last_name__icontains=q)|
                                         Q(company_name__icontains=q)|
                                         Q(city__icontains=q)|
                                         Q(phone_number__icontains=q))
        else:
            return Client.objects.all()
    
    def get_search_query(self):
        q = ''
        if 'q' in self.request.GET and self.request.GET['q']:
            q = self.request.GET['q'].strip()
        return q

    def get_context_data(self):
        context = super(ClientListView, self).get_context_data()
        context['q'] = self.get_search_query()
        return context


class ClientAddView(CreateView):
    template_name = "person/client/form.html"
    queryset = Client.objects.all()
    form_class = ClientForm
    success_url = 'client-details'
    
    def get_success_url(self):
        return reverse(self.success_url, kwargs={'pk': self.object.id})

    def form_invalid(self, form):
        html = loader.render_to_string(self.template_name, 
                                       dictionary=self.get_context_data(form=form), 
                                       context_instance=RequestContext(self.request))
        json = simplejson.dumps({'success': False, 'data': html})
        return HttpResponse(json)

    def form_valid(self, form):
        new_client = form.save()
        success_url = reverse('client-details', kwargs={'pk': new_client.id})
        json = simplejson.dumps({'success': True, 'data': success_url})
        return HttpResponse(json)


class ClientEditView(UpdateView):
    template_name = "person/client/form.html"
    form_class = ClientForm
    queryset = Client.objects.all()
    
    def get_success_url(self):
        return reverse('client-details', kwargs={'pk': self.get_object().id})

    def form_invalid(self, form):
        html = loader.render_to_string(self.template_name, 
                                       dictionary=self.get_context_data(form=form), 
                                       context_instance=RequestContext(self.request))
        json = simplejson.dumps({'success': False, 'data': html})
        return HttpResponse(json)

    def form_valid(self, form):
        super(ClientEditView, self).form_valid(form)
        json = simplejson.dumps({'success': True, 'data': self.get_success_url()})
        return HttpResponse(json)

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


class ClientAjaxSearch(TemplateView):
    template_name = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return TemplateView.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        q = request.GET.get('term')
        clients = Client.objects.filter(Q(first_name__icontains=q)|
                                        Q(last_name__icontains=q)|
                                        Q(company_name__icontains=q)|
                                        Q(city__icontains=q)|
                                        Q(phone_number__icontains=q))
        data = []
        for client in clients:
            label = str(client)
            if client.city:
                label = '%s (%s)' % (str(client), smart_str(client.city).strip())
            data.append({'id': client.id, 'label': label})
        return HttpResponse(simplejson.dumps(data))
