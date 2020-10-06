# import required libraries
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from . import models

# serializer used for login endpoint
class CustomerLoginSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=300, required=True)
	password = serializers.CharField(required=True, write_only=True)

# serializer for authenticating the customer and generating their auth_token
class AuthCustomerSerializer(serializers.ModelSerializer):
	auth_token = serializers.SerializerMethodField()
	class Meta:
		model = models.Customer
		fields = ('email', 'firstname', 'country', 'auth_token')
		extra_kwargs = {'password' : {'write_only': True}, 'auth_token':{'read_only': True}}
    
	# returns auth token based on user credentials
	def get_auth_token(self, obj):
		try:
			token = Token.objects.get(user_id=obj)
		except Token.DoesNotExist:
			token = Token.objects.create(user=obj)
		return token.key

# empty serializer for logout endpoint
class EmptySerializer(serializers.Serializer):
	pass    

# serializer for customer registration endpoint
class CustomerRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Customer
		fields = ('country', 'email', 'firstname','password', 'auth_token')
		extra_kwargs = {'password' : {'write_only': True}, 'auth_token':{'read_only': True}}
	
	# creates the object to be stored in Customer model
	def create(self, validated_data):
		user = models.Customer.objects.create_user(validated_data['email'],
		validated_data['firstname'], validated_data['country'], validated_data['password']
		)
		return user

# serializer to list, add book collection for the authorized user 		
class BookCollectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.BookCollection
		fields = ('title', 'author', 'isbn','date_added')

# serializer to filter/search books added in last N days in the collection 
# for the authorized user		
class BookFilterSerializer(serializers.ModelSerializer):
	books_added_since_last = serializers.IntegerField(max_value=30, min_value=1, help_text='Enter number of days', write_only=True, required=True)
	class Meta:
		model = models.BookCollection
		fields = ('date_added', 'books_added_since_last')
		read_only_fields = ['title', 'isbn', 'author']

# serializer to delete book from the collection for the authorized user		
class BookDeleteSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.BookCollection
		fields = ('isbn',)
		read_only_fields = ['email']		
		
