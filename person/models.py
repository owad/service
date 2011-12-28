# -* - coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.core.validators import RegexValidator

class User(AuthUser):
    class Meta:
        proxy = True

    def get_user_choices(self):
        users = User.objects.all()
        choices = {}
        for user in users:
            choices[user.id] = user.get_full_name()
        return choices.items()

    def __unicode__(self):
        return self.get_full_name()

class Client(models.Model):
    first_name = models.CharField(max_length=64, verbose_name='imię')
    last_name = models.CharField(max_length=128, verbose_name='nazwisko')
    company_name = models.CharField(max_length=128, blank=True, verbose_name='firma')
    address_line1 = models.CharField(max_length=128, blank=True, verbose_name='adres 1')
    address_line2 = models.CharField(max_length=128, blank=True, verbose_name='adres 2')
    city = models.CharField(blank=True, max_length=128, verbose_name='miejscowość')
    postcode = models.CharField(max_length=8, blank=True, verbose_name='kod pocztowy')
    email = models.EmailField(blank=True, verbose_name='e-mail')
    phone_number = models.CharField(max_length=9, verbose_name='telefon', validators=[RegexValidator('^(\d{9})$')])
    second_phone_number = models.CharField(max_length=9, verbose_name='telefon dodatkowy', validators=[RegexValidator('^(\d{9})$')], blank=True)
    is_subscriber = models.BooleanField(default=False, verbose_name='abonament serwisowy')
    created = models.DateTimeField(auto_now_add=True, verbose_name='data utworzenia')

    class Meta:
        verbose_name = "klient"
        verbose_name_plural = "klienci"
        ordering = ['-created']
    
    def __unicode__(self):
        if self.company_name: return self.company_name
        else: return "%s %s" % (self.first_name, self.last_name)

    def get_phone_numbers(self):
        numbers = []
        if self.phone_number:
            numbers.append(self.phone_number)
        if self.second_phone_number:
            numbers.append(self.second_phone_number)
        return ', '.join(numbers)
    
    def get_address_lines(self):
        address = []
        # yes, I know I'm not using keys
        for value in [self.address_line1, self.address_line2, self.postcode, self.city]:
            if value:
                address.append(value)
        return address