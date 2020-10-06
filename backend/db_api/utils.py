from django.contrib.auth import authenticate
from rest_framework import serializers
from . import models
from datetime import datetime, timedelta

def get_and_authenticate_customer(email, password):
	customer = authenticate(username=email, password=password)
	
	if customer is None:
		raise serializers.ValidationError("Invalid email/password. Please try again!")
	return customer
	
def create_customer_account(email, password, firstname="", country=""):
	user = models.Customer.objects.create_user(email=email, password=password, firstname=firstname, country=country)
	return user

def calc_time_diff(books_added_since_last):
	diff_date = datetime.utcnow() - timedelta(days=books_added_since_last)
	diff_date = diff_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
	
	return diff_date
	
