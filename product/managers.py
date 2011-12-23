from datetime import datetime, timedelta

from django.db.models import Q
from django.db import models


class OutdatedManager(models.Manager):

    def get_out_of_date(self, status, user):
        from models import Comment, Product
        if status == 'moje':
            product_ids = Comment.objects.filter(user=user, status=Product.PROCESSING, type=Comment.STATUS_CHANGE).values_list('product_id', flat=True)
            return Product.objects.filter(id__in=product_ids)
        elif status == 'przeterminowane':
            return Product.objects.filter(Q(updated__lte=datetime.now() - timedelta(days=3), status__in=(Product.NEW, Product.PROCESSING, Product.COURIER))|
                                          Q(updated__lte=datetime.now() - timedelta(days=7), status=Product.READY)|
                                          Q(updated__lte=datetime.now() - timedelta(days=10), status=Product.EXTERNAL))
        elif status == 'moje_przeterminowane':
            product_ids = Comment.objects.filter(user=user, status=Product.PROCESSING, type=Comment.STATUS_CHANGE).values_list('product_id', flat=True)
            products = Product.objects.filter(id__in=product_ids)
            return products.filter(Q(updated__lte=datetime.now() - timedelta(days=3), status__in=(Product.NEW, Product.PROCESSING, Product.COURIER))|
                                   Q(updated__lte=datetime.now() - timedelta(days=7), status=Product.READY)|
                                   Q(updated__lte=datetime.now() - timedelta(days=10), status=Product.EXTERNAL))

    def get_by_status_and_user(self, status, user):
        from models import Product
        if status in ['moje', 'przeterminowane', 'moje_przeterminowane']:
            return self.get_out_of_date(status, user)
        else:
            queryset = Product.objects.all().filter(status__exact=status)
            if queryset.count() > 0:
                return queryset
            else:
                return Product.objects.all()

    def get_closed(self):
        from models import Comment, Product
        product_ids = Comment.objects.filter(status__in=(Product.CLOSED, Product.READY), type=Comment.STATUS_CHANGE).values_list('product_id', flat=True)
        return Product.objects.filter(id__in=product_ids, status=Product.CLOSED)


    def get_ready(self):
        from models import Comment, Product
        product_ids = Comment.objects.filter(status__in=(Product.CLOSED, Product.READY), type=Comment.STATUS_CHANGE).values_list('product_id', flat=True)
        return Product.objects.filter(id__in=product_ids, status=Product.READY)
