# -*- coding: utf-8 -*-
from time import time

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

from user.models import User
from user.forms import UserForm
from product.views import ProductListView

from settings import USERS_PER_PAGE


class UserListView(ListView):
    context_object_name = "user_list"
    queryset = None
    template_name = "user/list.html"
    paginate_by = USERS_PER_PAGE
    
    def get_queryset(self):
        q = self.get_search_query()
        if q:
            return User.objects.filter(Q(first_name__icontains=q)|
                                         Q(last_name__icontains=q)|
                                         Q(company_name__icontains=q)|
                                         Q(city__icontains=q)|
                                         Q(phone_number__icontains=q))
        else:
            return User.objects.all()
    
    def get_search_query(self):
        q = None
        if 'q' in self.request.GET and self.request.GET['q']:
            q = self.request.GET['q'].strip()
        return q


class UserAddView(CreateView):
    template_name = "user/form.html"
    queryset = User.objects.all()
    form_class = UserForm
    success_url = 'user-details'
    
    def get_success_url(self):
        return reverse(self.success_url, kwargs={'pk': self.object.id})

    def get_initial(self):
        initial = self.initial.copy()
        initial['username'] = '%s_%s' % ('user', str(time()).replace('.', ''))
        return initial


class UserEditView(UpdateView):
    template_name = "user/form.html"
    form_class = UserForm
    queryset = User.objects.all()
    
    def get_success_url(self):
        return reverse('user-details', kwargs={'pk': self.get_object().id})

    '''
    def form_invalid(self, form):
        html = loader.render_to_string(self.template_name, 
                                       dictionary=self.get_context_data(form=form), 
                                       context_instance=RequestContext(self.request))
        json = simplejson.dumps({'success': False, 'data': html})
        return HttpResponse(json)

    def form_valid(self, form):
        super(UserEditView, self).form_valid(form)
        json = simplejson.dumps({'success': True, 'data': self.get_success_url()})
        return HttpResponse(json)
    '''

class UserDetailView(ProductListView):
    template_name = "user/details.html"
    
    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user.product_set.all()
    
    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        context['client'] = user
        return context


class UserAjaxSearch(TemplateView):
    template_name = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return TemplateView.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        q = request.GET.get('term')
        users = User.objects.filter(Q(first_name__icontains=q)|
                                        Q(last_name__icontains=q)|
                                        Q(company_name__icontains=q)|
                                        Q(city__icontains=q)|
                                        Q(phone_number__icontains=q))
        data = []
        for user in users:
            label = str(user)
            if user.city:
                label = '%s (%s)' % (str(user), smart_str(user.city).strip())
            data.append({'id': user.id, 'label': label})
        return HttpResponse(simplejson.dumps(data))
