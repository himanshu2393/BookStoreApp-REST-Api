# -- FILE: features/steps/search_steps.py
from behave import given, when, then, step
from django.test import TestCase
from datetime import datetime, timedelta
import json
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from db_api import models, serializers, views, utils, google_books_validator
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient, force_authenticate
from django.core.serializers.json import DjangoJSONEncoder

@given('the user is logged in and has not added any books in last N days')
def step_impl(context):
	# Create one user
	context.client = APIClient()
	test_user1 = models.Customer.objects.create_user(email='testuser1@email.com', password='abc@123', firstname='test1', country='Australia')
	test_user1.save()
	
	# generating token for user
	context.user = test_user1
	context.token = Token.objects.create(user=context.user)
	context.token.save()
	
	# authenticating the user
	context.client.force_authenticate(context.user, context.token.key)
		
@when('user enters the number of days')
def step_impl(context): 
	# creating payload to be passed to the endpoint
	context.payload = {'books_added_since_last':1}
	context.client.force_authenticate(context.user)

@then("gets empty records")
def step_impl(context):
	# calculating the date from which the records are to be fetched.
	diff_date = utils.calc_time_diff(context.payload['books_added_since_last'])
	# querying the endpoint
	context.client.post('/api/v1/bookcollection/search/', context.payload, HTTP_AUTHORIZATION=context.token)
	# querying the model
	exists = models.BookCollection.objects.filter(email = context.user).filter(date_added__gte=diff_date).exists()
	assert False is exists
	
# --- Scenario-2 -----------

@given('the user is logged in and has books added in last N days')
def step_impl(context):
	# Create one user
	context.client = APIClient()
	test_user1 = models.Customer.objects.create_user(email='testuser1@email.com', password='abc@123', firstname='test1', country='Australia')
	test_user1.save()

	# generating token for user
	context.user = test_user1
	context.token = Token.objects.create(user=context.user)
	context.token.save()
	
	# authenticating the user
	context.client.force_authenticate(context.user, context.token.key)
	
	# Add a book in the collection of test_user1 created above
	test_book = models.BookCollection.objects.create(
		title='D Is for Dragon Fruit',
		isbn='9780615380100',
		author='Monique Duncan',
		email=context.user)

	test_book.save()	
		
@when('user enters number of days')
def step_impl(context): 
	# creating payload to be passed to the endpoint
	context.payload = {'books_added_since_last':1}
	context.client.force_authenticate(context.user)

@then("user gets filtered records")
def step_impl(context):
	# calculating the date from which the records are to be fetched
	diff_date = utils.calc_time_diff(context.payload['books_added_since_last'])
	# querying the endpoint
	context.client.post('/api/v1/bookcollection/search/', context.payload, HTTP_AUTHORIZATION=context.token)
	# querying the model
	exists = models.BookCollection.objects.filter(email = context.user).filter(date_added__gte=diff_date).exists()
	assert True is exists
	
# -- Scenario 3 -------------

@given('the user is logged in and has books in collection')
def step_impl(context):
	# Create one user
	context.client = APIClient()
	test_user1 = models.Customer.objects.create_user(email='testuser1@email.com', password='abc@123', firstname='test1', country='Australia')
	test_user1.save()

	# generating token for user
	context.user = test_user1
	context.token = Token.objects.create(user=context.user)
	context.token.save()
	
	# authenticating the user
	context.client.force_authenticate(context.user, context.token.key)
	
	# Add a book in the collection of test_user1 created above
	test_book = models.BookCollection.objects.create(
		title='D Is for Dragon Fruit',
		isbn='9780615380100',
		author='Monique Duncan',
		email=context.user)

	test_book.save()	
		
@when('user enters number of days as less than 1')
def step_impl(context): 
	context.payload = {'books_added_since_last':-1}
	context.client.force_authenticate(context.user)

@then("user gets response error bad request.")
def step_impl(context):
	res = context.client.post('/api/v1/bookcollection/search/', context.payload, HTTP_AUTHORIZATION=context.token)
	assert res.status_code == 400
	
# -- Scenario -4 -----------

@given('the user is logged in and has books added in collection')
def step_impl(context):
	# Create one user
	context.client = APIClient()
	test_user1 = models.Customer.objects.create_user(email='testuser1@email.com', password='abc@123', firstname='test1', country='Australia')
	test_user1.save()
	
	# generating token for the user
	context.user = test_user1
	context.token = Token.objects.create(user=context.user)
	context.token.save()
	
	# authenticating the user
	context.client.force_authenticate(context.user, context.token.key)
	
	# Add a book in the collection of test_user1 created above
	test_book = models.BookCollection.objects.create(
		title='D Is for Dragon Fruit',
		isbn='9780615380100',
		author='Monique Duncan',
		email=context.user)

	test_book.save()	
		
@when('user enters number of days more than 30')
def step_impl(context): 
	context.payload = {'books_added_since_last':31}
	context.client.force_authenticate(context.user)

@then("user gets error bad request.")
def step_impl(context):
	res = context.client.post('/api/v1/bookcollection/search/', context.payload, HTTP_AUTHORIZATION=context.token)
	assert res.status_code == 400
	
