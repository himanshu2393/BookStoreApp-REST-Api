# -- FILE: features/steps/list_all_books_steps.py
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

@given('the user is logged in with books in his/her collection')
def step_impl(context):
	# Create one user
	context.client = APIClient()

	test_user1 = models.Customer.objects.create_user(email='testuser1@email.com', password='abc@123', firstname='test1', country='Australia')
	test_user1.save()

	context.user = test_user1
	context.token = Token.objects.create(user=context.user)
	context.token.save()
	context.client.force_authenticate(context.user, context.token.key)
		

@when('user visits the url /api/v1/bookcollection/')
def step_impl(context): 
	context.client.force_authenticate(context.user)

@then('gets all the books returned with response status as 200.')
def step_impl(context):
	response = context.client.get(reverse('collection-list'), HTTP_AUTHORIZATION=context.token)
	print(response.status_code)
	assert response.status_code == 200

# --- Scenario -2 ----------

@given('the user is not logged in')
def step_impl(context):
	context.client = APIClient()
	test_user1 = models.Customer.objects.create_user(email='testuser1@email.com', password='abc@123', firstname='test1', country='Australia')
	test_user1.save()
	context.user = test_user1
	context.token = Token.objects.create(user=context.user)
	context.token.save()
	#context.client.force_authenticate(context.user, context.token.key)

@when('user visits url /api/v1/bookcollection/')
def step_impl(context):
	pass
	#context.client.force_authenticate(context.user)

@then('user gets authentication error')
def step_impl(context):
	response = context.client.get(reverse('collection-list'))
	assert response.status_code == 401
	
	
