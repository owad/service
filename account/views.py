# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.contrib.auth.forms import PasswordChangeForm

class Profile(TemplateView):
    template_name = "account/profile.html"
    
    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['user_change_form'] = PasswordChangeForm(self.request.user)
        return context