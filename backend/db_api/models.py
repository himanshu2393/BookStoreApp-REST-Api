from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
from .google_books_validator import *
from django.conf import settings

from .managers import CustomUserManager

# Create your models here.
class Customer(AbstractUser):
	username = None
	first_name = None
	email = models.EmailField(max_length = 250, primary_key=True)	
	
	USERNAME_FIELD = 'email'
	FIRST_NAME_FIELD = 'firstname'
	
	objects = CustomUserManager()
	
	firstname = models.CharField(max_length=50)
	country = CountryField(blank_label='(select country)')
	REQUIRED_FIELDS = []
	
	def __str__(self):
		return self.email

class BookCollection(models.Model):
	title = models.CharField(max_length=200)
	author = models.CharField(max_length=200)
	isbn = models.CharField(max_length=13)
	email = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customer_email', on_delete=models.CASCADE)
	date_added = models.DateTimeField(auto_now=True)
	
	class Meta:
		unique_together = ("email", "isbn")

	