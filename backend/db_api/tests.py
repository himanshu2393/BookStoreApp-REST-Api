from django.test import TestCase
from datetime import datetime, timedelta
import json
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from . import models, serializers, views, utils
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient, force_authenticate
from django.core.serializers.json import DjangoJSONEncoder


# test the bookcollection API endpoint and its actions generated
class BookCollectionListSearchViewSetTest(TestCase):
	def setUp(self):
		# Create two users
		self.client = APIClient()
		test_user1 = models.Customer.objects.create_user(email='testuser1@email.com', password='abc@123', firstname='test1', country='Australia')
		test_user2 = models.Customer.objects.create_user(email='testuser2@email.com', password='abc@123', firstname='test2', country='Australia')
			
		test_user1.save()
		test_user2.save()

		self.user = test_user1
		self.token = Token.objects.create(user=self.user)
		self.token.save()
		self.client.force_authenticate(self.user, self.token.key)
		
		# Add a book in the collection of test_user1 created above
		test_book = models.BookCollection.objects.create(
			title='D Is for Dragon Fruit',
			isbn='9780615380100',
			author='Monique Duncan',
			email=self.user)

		test_book.save()		
        
	# tests the book returned for the logged in user or list functionality 
	def test_bookcollection_list(self):
		# get response from the api-endpoint
		response = self.client.get(reverse('collection-list'))

		# get all books of test_user1 from database model
		all_books = models.BookCollection.objects.all()
		all_books.values()[0]['date_added'] = datetime.strptime(datetime.strftime(all_books.values()[0]['date_added'], '%Y-%m-%dT%H:%M:%S.%fZ'), '%Y-%m-%dT%H:%M:%S.%fZ')
		
		data = json.dumps(list(all_books.values('title', 'author', 'isbn', 'email','date_added')), cls=DjangoJSONEncoder)
		data = json.loads(data)
		data[0]['date_added'] = datetime.strptime(datetime.strftime(all_books.values()[0]['date_added'], '%Y-%m-%dT%H:%M:%S.%fZ'), '%Y-%m-%dT%H:%M:%S.%fZ').isoformat()+'Z'
		new_data=[]
		
		for rec in data:
			serializer = serializers.BookCollectionSerializer(data=rec)
			if serializer.is_valid():
				serializer.validated_data["date_added"] = serializer.initial_data["date_added"]
				new_data.append(serializer.validated_data)
		
		# Compare the response object and serializer object to verify the testcase
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, new_data)

	# tests the functionality of adding a book in the user's collection 
	def test_bookcollection_add_book(self):
		payload = {'title': 'alpha', 'author':'beta', 'isbn':'9789881219565'}
		self.client.force_authenticate(self.user)
		
		# sending a post request with token authentication  (it should verify the ISBN from GoogleBooks API 
		# and then correct title & author before inserting)
		self.client.post(reverse('collection-list'), payload, HTTP_AUTHORIZATION=self.token)
		
		# chechking if the book exists after sending the post request to the endpoint. 
		# exists() function will return boolean true or false value
		exists = models.BookCollection.objects.filter(
			email = self.user,
			isbn = payload['isbn'],
		).exists() 
		
		self.assertTrue(exists)
	
	# tests the deletion of book record from the collection of the user
	def test_bookcollection_del_book(self):
		payload = {'isbn':'9789881219565'}
		self.client.force_authenticate(self.user)
		
		# sending a post request with token authentication  
		#(looks for the book in test_user1's collection based on ISBN number and delete that record)  
		self.client.post(reverse('collection-list')+'delete_record', payload, HTTP_AUTHORIZATION=self.token)
		
		#checking if the book exists after sending the delete request to the endpoint. 
		# exists() function will return boolean true or false value
		exists = models.BookCollection.objects.filter(email = self.user).filter(isbn = payload['isbn']).exists()
		
		# asserting false i.e. book should not exists after deleteion to pass this test.
		self.assertFalse(exists)
	
	# test the search functionality to look for books added in the collection since last 7,14 etc. days (passed in payload)
	def test_bookcollection_search_by_days(self):
		payload = {'books_added_since_last':1}
		
		self.client.force_authenticate(self.user)
		
		# sending a post request with token authentication  
		#(search for the books in test_user1's collection based on books_added_since_last number of days and return filtered records)  
		response = self.client.post('/api/v1/bookcollection/search/', payload, HTTP_AUTHORIZATION=self.token)

		# querying the database model for the same search query books_added_since_last number of days
		diff_date = utils.calc_time_diff(payload['books_added_since_last'])
		qryset = models.BookCollection.objects.filter(email = self.user).filter(date_added__gte=diff_date)
		
		data = json.dumps(list(qryset.values('title', 'author', 'isbn', 'email','date_added')), cls=DjangoJSONEncoder)
		data = json.loads(data)
		new_data=[]
		
		for rec in data:
			#rec['date_added'] = datetime.strptime(rec['date_added'], '%Y-%m-%dT%H:%M:%S.%fZ').isoformat()+'Z'
			serializer = serializers.BookCollectionSerializer(data=rec)
			if serializer.is_valid():
				serializer.validated_data["date_added"] = serializer.initial_data["date_added"]
				new_data.append(serializer.validated_data)
		
		# Compare the response object and serializer object to verify the testcase
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, new_data)

    
		
		
		
