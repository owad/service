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

    def get_for_report(self, get_data):
        from models import Comment, Product, User
        
        if get_data:
            date_pattern = '%Y-%m-%d %H:%M:%S'
            startdate = datetime.strptime('%s-%s-%s 00:00:00' % (get_data['start_date_year'], get_data['start_date_month'], get_data['start_date_day']), date_pattern)
            enddate = datetime.strptime('%s-%s-%s 23:59:59' % (get_data['end_date_year'], get_data['end_date_month'], get_data['end_date_day']), date_pattern)
            
            users = User.objects.filter(pk__in=get_data.getlist('user'))
            
            # get all products owned by provided users
            owned_products = Comment.objects.filter(status=Product.PROCESSING,
                                                 type=Comment.STATUS_CHANGE,
                                                 user__in=users
                                                 ).values_list('product_id', flat=True)
            # get products finished and closed during provided dates
            closed_products = Comment.objects.filter(status=Product.CLOSED,
                                                 type=Comment.STATUS_CHANGE,
                                                 created__range=(startdate, enddate)).values_list('product_id', flat=True)
            
            # getting proper products for reports
            product_ids = set(owned_products) & set(closed_products)
            # filtering by warranty flag
            return Product.objects.filter(id__in=product_ids, warranty__in=get_data.getlist('warranty'))
        return []
