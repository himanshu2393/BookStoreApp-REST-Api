from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model, logout
from django_filters import rest_framework as filters
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status, viewsets
from .models import Customer, BookCollection
from .utils import *
from .google_books_validator import *
import json
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.core import serializers as core_serializer
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q

from . import serializers
from . import models
from django.http import Http404

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Creating viewsets here.
class RegisterViewSet(ModelViewSet):
	"""Add a user here. (Only superuser can see other user details and logged out users can register as new users.)"""
	model = models.Customer
	permission_classes = [AllowAny, ]
	serializer_class = serializers.CustomerRegisterSerializer
	serializer_classes = {
		'register': serializers.CustomerRegisterSerializer,
    }
	
	def get_queryset(self):
		user = self.request.user
		if user.is_superuser:
			queryset = Customer.objects.all()
			return queryset
		else:
			return None
	
	def create(self, request):
		user = self.request.user
		if str(user) == 'AnonymousUser':
			serializer = self.get_serializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			user = create_customer_account(**serializer.validated_data)
			data = serializers.AuthCustomerSerializer(user).data
			return Response(data=data, status=status.HTTP_201_CREATED)
		else:
			return Response(data={'You need to logout before registering as new user.'}, status=status.HTTP_401_UNAUTHORIZED)
	
	def get_serializer_class(self):
		if not isinstance(self.serializer_classes, dict):
			raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

		if self.action in self.serializer_classes.keys():
			return self.serializer_classes[self.action]
		return self.serializer_class #super().get_serializer_class()
	
	def get_serializer_context(self):
		"""
		Extra context provided to the serializer class.
		"""
		return {
			'request': self.request,
			'view': self,
        }
		
	def get_serializer(self, *args, **kwargs):
		"""
		Return the serializer instance that should be used for validating and
		deserializing input, and for serializing output.
		"""
		serializer_class = self.get_serializer_class()
		kwargs['context'] = self.get_serializer_context()
		return serializer_class(*args, **kwargs)

	
class BookCollectionViewSet(ModelViewSet):
	"""
      Add Books here and see your collection so far... (Check 'Extra Actions' for more)	
	"""
	
	model = models.BookCollection
	
	serializer_class = serializers.BookCollectionSerializer
	serializer_classes = {
        'search': serializers.BookFilterSerializer,
		'delete_record': serializers.BookDeleteSerializer,
    }
	permission_classes = (IsAuthenticated,)
		
	def get_queryset(self):
		user = self.request.user
		queryset = BookCollection.objects.filter(email=user)
		return queryset
		
	def create(self, request):
		#print("Add Book:",request.user.auth_token)

		serializer = self.serializer_class(data=request.data)
		
		user = request.user
		# verifying and correcting with Google Books API
		parsed_response = get_book_details_seq(request.data['isbn'])
				
		if serializer.is_valid():
			if parsed_response[0] != None:
				book = {'title':parsed_response[0],'author':', '.join([str(authr) for authr in parsed_response[1]]),'isbn':request.data['isbn']}
				serializer = serializers.BookCollectionSerializer(data=book)			
				
				if serializer.is_valid():					
					serializer.save(email=request.user)
					return Response(serializer.validated_data, status=status.HTTP_201_CREATED)	
				else:
					return Response({
						'status': 'Bad request',
						'message': 'Book could not be added with received data.'
					}, status=status.HTTP_400_BAD_REQUEST)
			
			else:
				raise BookNotFound()
		else:
			return Response({
				'status': 'Bad request',
				'message': 'Book could not be added with received data.'
			}, status=status.HTTP_400_BAD_REQUEST)

	@action(methods=['POST', ], detail=False)
	def delete_record(self, request):
		serializer = self.serializer_class(data=request.data)
		user = request.user
		print(user)
		print(request.data['isbn'])
		 
		try:
			instance = BookCollection.objects.filter(Q(email=user) & Q(isbn=request.data['isbn']))
			data = json.dumps(list(instance.values('title', 'author', 'isbn', 'email','date_added')), cls=DjangoJSONEncoder)
			data = json.loads(data)
			
			self.perform_destroy(instance)
			
			new_data = list()
			for rec in data:
				serializer = serializers.BookCollectionSerializer(data=rec, partial=True)
				if serializer.is_valid():
					new_data.append(serializer.validated_data)

			if serializer.is_valid():
				return Response(new_data, status=status.HTTP_200_OK)	
			else:
				return Response({
					'status': 'Bad request',
					'message': 'Book could not be deleted. Check the ISBN you entered.'
				}, status=status.HTTP_400_BAD_REQUEST)
		except Http404:
			pass
		return Response(status=status.HTTP_204_NO_CONTENT)
	
	@action(methods=['POST', ], detail=False)
	def search(self, request):	
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		diff_date = calc_time_diff(**serializer.validated_data)
		records = self.get_queryset().filter(date_added__gte=diff_date)
		
		data = json.dumps(list(records.values('title', 'author', 'isbn', 'email','date_added')), cls=DjangoJSONEncoder)
		data = json.loads(data)
		new_data = list()
		for rec in data:
			serializer = serializers.BookCollectionSerializer(data=rec, partial=True)
			if serializer.is_valid():
				serializer.validated_data["date_added"] = serializer.initial_data["date_added"]
				new_data.append(serializer.validated_data)

		if serializer.is_valid():
			return Response(new_data, status=status.HTTP_200_OK)	
		else:
			return Response({
				'status': 'Bad request',
				'message': 'Book could not be added with received data.'
			}, status=status.HTTP_400_BAD_REQUEST)

	def get_serializer_class(self):
		if not isinstance(self.serializer_classes, dict):
			raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

		if self.action in self.serializer_classes.keys():
			return self.serializer_classes[self.action]
		return self.serializer_class #super().get_serializer_class()
	
	def get_serializer_context(self):
		"""
		Extra context provided to the serializer class.
		"""
		return {
			'request': self.request,
			'view': self,
		}
		
	def get_serializer(self, *args, **kwargs):
		"""
		Return the serializer instance that should be used for validating and
		deserializing input, and for serializing output.
		"""
		serializer_class = self.get_serializer_class()
		kwargs['context'] = self.get_serializer_context()
		return serializer_class(*args, **kwargs)






