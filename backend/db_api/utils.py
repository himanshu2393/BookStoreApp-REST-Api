# import required libraries
from django.contrib.auth import authenticate
from rest_framework import serializers
from . import models
from datetime import datetime, timedelta

# authenticates the customer using email and pass 
def get_and_authenticate_customer(email, password):
	customer = authenticate(username=email, password=password)
	
	if customer is None:
		raise serializers.ValidationError("Invalid email/password. Please try again!")
	return customer

# creates a customer object to be stored in the model or database	
def create_customer_account(email, password, firstname="", country=""):
	user = models.Customer.objects.create_user(email=email, password=password, firstname=firstname, country=country)
	return user

# calculates the diff between current date and the N (number of days)
# to get final date value (let's say today is 25th Jun - 2 days gives 23rd Jun) 
# to be used for search filter
def calc_time_diff(books_added_since_last):
	diff_date = datetime.utcnow() - timedelta(days=books_added_since_last)
	diff_date = diff_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
	
	return diff_date
	
