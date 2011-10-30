# -* - coding: utf-8 -*-
from django.db import models
from django.db.models import Sum, Count

from person.models import User, Client

class Courier(models.Model):
    
    name = models.CharField(max_length='64')
    
    class Meta:
        verbose_name_plural = "kurierzy"
        verbose_name = "kurier"
    
    def __unicode__(self):
        return self.name
    
class Product(models.Model):
    DECIMAL_ZERO = '0.00'
    NEW, PROCESSING, COURIER = ('przyjety', 'w_realizacji', 'do_wyslania')
    EXTERNAL, READY, CLOSED = ('w_serwisie', 'do_wydania', 'wydany')
    STATUSES = (NEW, PROCESSING, COURIER, EXTERNAL, READY, CLOSED)
    
    NEW_PLURAL, PROCESSING_PLURAL, COURIER_PLURAL = ('przyjęty', 'w realizacji', 'do wysłania')
    EXTERNAL_PLURAL, READY_PLURAL, CLOSED_PLURAL = ('w serwisie', 'do wydania', 'wydany')
    STATUS_CHOICES = (
        (NEW, NEW_PLURAL),
        (PROCESSING, PROCESSING_PLURAL),
        (COURIER, COURIER_PLURAL),
        (EXTERNAL, EXTERNAL_PLURAL),
        (READY, READY_PLURAL),
        (CLOSED, CLOSED_PLURAL)
    )
    
    FIRST_STATUS = NEW
    LAST_STATUS = CLOSED
    
    Y, N = ('Y', 'N')
    Y_PLURAL, N_PLURAL = ('Tak', 'Nie')
    WARRANTY_CHOICES = ( 
        (N, N_PLURAL),
        (Y, Y_PLURAL)
    )

    name = models.CharField(max_length=128, verbose_name='nazwa')
    producent = models.CharField(max_length=128, blank=True, verbose_name='producent')
    serial = models.CharField(max_length=128, blank=True, verbose_name='numer seryjny')
    invoice = models.CharField(max_length=128, blank=True, verbose_name='numer faktury')
    description = models.TextField(blank=True, verbose_name='opis usterki')
    status = models.CharField(choices=STATUS_CHOICES, max_length=32)
    parcel_number = models.CharField(max_length=64, blank=True, verbose_name='numer przesyłki')
    external_service_name = models.CharField(max_length=128, blank=True, verbose_name='nazwa serwisu zewnętrznego')
    max_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='koszt naprawy do', default=DECIMAL_ZERO)
    warranty = models.CharField(choices=WARRANTY_CHOICES, max_length=16, verbose_name='gwarancja')
    courier = models.IntegerField(null=True, blank=True, choices=[(obj.id, obj) for obj in Courier.objects.all()])
    created = models.DateTimeField(auto_now_add=True, verbose_name='data zgłoszenia')
    updated = models.DateTimeField(auto_now=True, verbose_name='ostatnia akutalizajca')
    
    user = models.ForeignKey(User, verbose_name='pracownik')
    client = models.ForeignKey(Client, verbose_name='klient')
    
    class Meta:
        verbose_name_plural = "zgłoszenia"
        verbose_name = "zgłoszenie"
        ordering = ['-created']
        
    def get_next_status(self):
        break_on_next = False
        next_status = self.FIRST_STATUS
        if self.status == self.LAST_STATUS: return self.LAST_STATUS
        if self.status == '': return self.FIRST_STATUS
        else: 
            for key, status in self.STATUS_CHOICES:
                if (break_on_next): 
                    next_status = key
                    break;
                if key == self.status: break_on_next = True
            return next_status
    
    def set_next_status(self, request):
        old_status = self.status 
        POST = request.POST
        if 'status_change' in POST and int(POST['status_change']) == 1 and self.status == self.PROCESSING:
            self.status = Product.READY
        else: 
            self.status = self.get_next_status()
        
        if old_status != self.status:
            new_comment = Comment()
            new_comment.note = 'Zmiana statusu na %s' % (self.get_status_name(),)
            new_comment.type = Comment.STATUS_CHANGE
            new_comment.user_id = request.user.id
            new_comment.product_id = POST['product']
            new_comment.save()
        
        if old_status == self.COURIER:
            self.parcel_number = POST['parcel_number']
            self.courier = POST['courier']
        
    def get_status_name(self):
        for status in self.STATUS_CHOICES:
            if self.status == status[0]: return status[1]
        return self.FIRST_STATUS
    
    def get_hardware_cost(self):
        return self.comment_set.aggregate(sum=Sum('hardware'))['sum']
        
    def get_software_cost(self):
        return self.comment_set.aggregate(sum=Sum('software'))['sum']
    
    def get_transport_cost(self):
        return self.comment_set.aggregate(sum=Sum('transport'))['sum']
    
    def get_cost(self):
        return self.get_hardware_cost() + self.get_software_cost() + self.get_transport_cost()
    
    def get_warranty_name(self):
        if self.warranty == self.N: return self.Y_PLURAL
        else: return self.N_PLURAL
    
    def save(self, *args, **kwargs):
        if self.warranty is None: self.warranty = self.N
        if self.status is None: self.status = self.FIRST_STATUS
        super(Product, self).save(*args, **kwargs)
    
    def get_counts(self):
        result = Product.objects.values('status').annotate(count=Count('status'))
        counts = {}
        all = 0
        for status in Product.STATUSES:
            counts[status] = 0
            for row in result:
                if status == row['status']:
                    counts[status] = row['count']
            all += counts[status]
        counts['wszystkie'] = all
        return counts
    
    def __unicode__(self):
        return self.name
    
class Comment(models.Model):
    COMMENT, STATUS_CHANGE, HARDWARE_ADD = ('komentarz', 'zmiana_statusu', 'sprzet')
    COMMENT_PLURAL, STATUS_CHANGE_PLURAL, HARDWARE_ADD_PLURAL = ('komenatrz', 'zmiana statusu', 'sprzęt')
    TYPES = (
        (COMMENT, COMMENT_PLURAL),
        (STATUS_CHANGE, STATUS_CHANGE_PLURAL),
        (HARDWARE_ADD, HARDWARE_ADD_PLURAL)
    )
    
    DECIMAL_ZERO = '0.00'
    
    note = models.TextField(verbose_name='notatka')
    type = models.CharField(choices=TYPES, max_length=32, verbose_name='typ')
    user = models.ForeignKey(User, verbose_name='pracownik')
    product = models.ForeignKey(Product, verbose_name='produkt')
    hardware = models.DecimalField(max_digits=10, decimal_places=2, default=DECIMAL_ZERO, verbose_name='koszt sprzętu')
    software = models.DecimalField(max_digits=10, decimal_places=2, default=DECIMAL_ZERO, verbose_name='koszt usługi')
    transport = models.DecimalField(max_digits=10, decimal_places=2, default=DECIMAL_ZERO, verbose_name='koszt dojazdu')
    created = models.DateTimeField(auto_now_add=True, verbose_name='data zgłoszenia')

    class Meta:
        verbose_name_plural = "komentarz"
        ordering = ['-created']
    
    def save(self, *args, **kwargs):
        if self.hardware is None: self.hardware = self.DECIMAL_ZERO
        if self.software is None: self.software = self.DECIMAL_ZERO
        if self.transport is None: self.transport = self.DECIMAL_ZERO
        super(Comment, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.note
    