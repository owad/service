# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render_to_response, get_object_or_404, render
from www.service.models import Product, Client, Comment
from django.contrib.auth.models import User
from www.service.forms import CommentForm, ProductForm, ClientForm, \
                            ReportForm, HardwareCommentForm
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


