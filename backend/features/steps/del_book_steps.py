# -- FILE: features/steps/del_book_steps.py
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

@given('the user is logged in and has the ISBN')
def step_impl(context):
	# Create one user
	context.client = APIClient()

	test_user1 = models.Customer.objects.create_user(email='testuser1@email.com', password='abc@123', firstname='test1', country='Australia')
	test_user1.save()

	context.user = test_user1
	context.token = Token.objects.create(user=context.user)
	context.token.save()
	context.client.force_authenticate(context.user, context.token.key)
	
	# Add a book in the collection of test_user1 created above
	test_book = models.BookCollection.objects.create(
		title='D Is for Dragon Fruit',
		isbn='9780615380100',
		author='Monique Duncan',
		email=context.user)

	test_book.save()	
		
@when('user enters wrong ISBN')
def step_impl(context): 
	context.incorrect_payload = {'isbn':'978061538010'}
	context.correct_payload = {'isbn':'9780615380100'}
	context.client.force_authenticate(context.user)

@then("book will not be deleted from the database from the user's collection")
def step_impl(context):
	context.client.post('/api/v1/bookcollection/delete_record/', context.incorrect_payload, HTTP_AUTHORIZATION=context.token)
	exists = models.BookCollection.objects.filter(email = context.user).filter(isbn = context.correct_payload['isbn']).exists()
	assert True is exists
	
# --- Scenario-2 -----------

@given('the user is logged in and has ISBN')
def step_impl(context):
	# Create one user
	context.client = APIClient()

	test_user1 = models.Customer.objects.create_user(email='testuser1@email.com', password='abc@123', firstname='test1', country='Australia')
	test_user1.save()

	context.user = test_user1
	context.token = Token.objects.create(user=context.user)
	context.token.save()
	context.client.force_authenticate(context.user, context.token.key)
	
	# Add a book in the collection of test_user1 created above
	test_book = models.BookCollection.objects.create(
		title='D Is for Dragon Fruit',
		isbn='9780615380100',
		author='Monique Duncan',
		email=context.user)

	test_book.save()	
		
@when('user enters correct ISBN')
def step_impl(context): 
	context.payload = {'isbn':'9780615380100'}
	context.client.force_authenticate(context.user)
	#assert True is not False

@then("book will be deleted from the database from the user's collection")
def step_impl(context):
	context.client.post('/api/v1/bookcollection/delete_record/', context.payload, HTTP_AUTHORIZATION=context.token)
	exists = models.BookCollection.objects.filter(email = context.user).filter(isbn = context.payload['isbn']).exists()
	assert False is exists
	
