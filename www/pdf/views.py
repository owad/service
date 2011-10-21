# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render_to_response, get_object_or_404, render
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q, Count
import datetime
from django.db.models import Sum
from django import template
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.contrib import messages
import ho.pisa as pisa
import cStringIO as StringIO

register = template.Library()

def html_pdf_preview(request, product_id, as_pdf=False):
    if request.user.is_authenticated() == False:
        return HttpResponseRedirect(reverse('product-list'))
    product = get_object_or_404(Product, pk=product_id)
    data = {'product': product, 'client': product.client, 'comment_list': product.comment_set.all()}
    if as_pdf:
        return data
    return render_to_response('service/product/print2.html', data, RequestContext(request))
    
def get_pdf(request, product_id):
    if request.user.is_authenticated() == False:
        return HttpResponseRedirect(reverse('product-list'))
    data = html_pdf_preview(request, product_id, as_pdf = True)
    file_data = render_to_string('service/product/print2.html', data, RequestContext(request))
    myfile = StringIO.StringIO()
    pisa.CreatePDF(file_data.encode('UTF-8'), myfile, encoding='UTF-8')
    myfile.seek(0)
    response =  HttpResponse(myfile, mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=zgloszenie_nr_%s.pdf' % (data['product'].id,)
    return response