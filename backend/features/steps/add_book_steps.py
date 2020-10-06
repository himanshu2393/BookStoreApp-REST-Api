# -- FILE: features/steps/add_book_steps.py
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

@given('the user is logged in and has the book details')
def step_impl(context):
	# Create one user
	context.client = APIClient()
	test_user1 = models.Customer.objects.create_user(email='testuser1@email.com', password='abc@123', firstname='test1', country='Australia')
	test_user1.save()

	# generating auth token for the user
	context.user = test_user1
	context.token = Token.objects.create(user=context.user)
	context.token.save()
	
	# authenticating the user
	context.client.force_authenticate(context.user, context.token.key)
		

@when('user enters wrong details & wrong ISBN')
def step_impl(context): 
	# creating a payload to pass to the endpoint
	context.payload = {'title': 'alpha', 'author':'beta', 'isbn':'978988121956'}
	context.client.force_authenticate(context.user)

@then('GoogleBooks API will reject')
def step_impl(context):
	# validating the book isbn entered with GoogleBooks API
	res = google_books_validator.get_book_details_seq(context.payload['isbn'])
	assert res[0] == None

@then('book will not be saved in the database.')
def step_impl(context):
	# querying the endpoint with the payload
	response = context.client.post(reverse('collection-list'), context.payload, HTTP_AUTHORIZATION=context.token)
	assert response.status_code == 400

# --- Scenario -2 ----------

@given('the user is logged in and has book details')
def step_impl(context):
	# creating a user
	context.client = APIClient()
	test_user1 = models.Customer.objects.create_user(email='testuser1@email.com', password='abc@123', firstname='test1', country='Australia')
	test_user1.save()
	
	# generating auth token for the user
	context.user = test_user1
	context.token = Token.objects.create(user=context.user)
	context.token.save()
	
	# authenticating the user
	context.client.force_authenticate(context.user, context.token.key)

@when('user enters correct ISBN and wrong details')
def step_impl(context):
	# creating the payload
	context.payload = {'title': 'alpha', 'author':'beta', 'isbn':'9789881219565'}
	context.client.force_authenticate(context.user)

@then('GoogleBooks API will return title and author to update book details')
def step_impl(context):
	# validating with GoogleBooks API for the passed ISBN as payload
	res = google_books_validator.get_book_details_seq(context.payload['isbn'])
	assert res[0] != None

@then('book will be saved in the database.')
def step_impl(context):
	# querying the endpoint
	response = context.client.post(reverse('collection-list'), context.payload, HTTP_AUTHORIZATION=context.token)
	assert response.status_code == 201
	
	
