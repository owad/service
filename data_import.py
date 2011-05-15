#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import site
site.addsitedir('/home/owad/company/lib/python2.6/site-packages')
 
path = '/srv/www/demo'
if path not in sys.path:
    sys.path.insert(0, '/srv/www/demo')
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'

import MySQLdb
from www.service import models
from datetime import datetime

def get_old_db():
	db =  MySQLdb.connect(user='company', db='serwis', passwd='uwreFTBhJCU3xjJb', host='localhost', use_unicode=True, charset='latin2')
	return db
	



def get_clients():
	db = get_old_db()
	cursor = db.cursor()
	cursor.execute('SELECT * FROM klient')
	return cursor.fetchall()

def get_products():
	db = get_old_db()
	cursor = db.cursor()
	cursor.execute('SELECT * FROM produkt')
	return cursor.fetchall()

def move_client(row):
	client = models.Client.objects.create(id=row[0], first_name=row[1], last_name=row[2], company_name=row[3], address_line1=row[4], address_line2='', city=row[5], postcode=row[6], email=row[7], phone_number=row[8])

def move_product(row):
	#product
	id = row[0]
	name = row[3]
	producent = row[4]
	serial = row[11]
	description = row[5]
	status = get_status(row[17], row[7])
	parcel_number = row[8]
	max_cost = row[12]
	if row[6] == 'tak': warranty = 'Y'
	else: warranty = 'N'
	user_id = row[2]
	client_id = row[1]
	created = row[19]
	updated = row[20]
	product = models.Product.objects.create(id=id, name=name, producent=producent, serial=serial, description=description, status=status, parcel_number=parcel_number, max_cost=max_cost, warranty=warranty, user_id=user_id, client_id=client_id, created=created, updated=updated)
	if created: product.created = created
	if updated: product.updated = updated
	product.save()
	#comment
	move_comments(row)

def get_status(old_status, external_service_status):
	if old_status == 0:
		return 'przyjety'
	if old_status == 1 and external_service_status == 0:
		return 'w_realizacji'
	if old_status == 1 and external_service_status == 1:
		return 'oczekiwanie_na_kuriera'
	if old_status == 1 and external_service_status == 2:
		return 'wyslano_do_serwisu_zew'
	if old_status == 2:
		return 'do_wydania'
	if old_status == 3:
		return 'wydany'

def move_comments(row):
	comments = row[18].split("\n")
	type = 'komentarz'
	user_id = row[2]
	product_id = row[0]
	hardware = row[14]
	software = row[15]
	transport = row[16]
	created = row[20]
	for note in comments:
		comment = models.Comment.objects.create(note=note, type=type, user_id=user_id, product_id=product_id, created=created)
	comment = models.Comment.objects.create(note='Koszy całkowity', type=type, user_id=user_id, product_id=product_id,  hardware=hardware ,software=software , transport=transport, created=created)
	if created: comment.created = created
	comment.save()

def process():
	sure = raw_input("Pewny? [y/n]")
	if (sure == 'y'):	
		models.Product.objects.all().delete()
		models.Client.objects.all().delete()
		models.Comment.objects.all().delete()
	
		for row in get_clients():
			move_client(row)
		for row in get_products():
			move_product(row)
process()
