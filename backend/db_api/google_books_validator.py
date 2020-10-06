import os
import requests
import json
from requests.exceptions import HTTPError
from rest_framework.exceptions import APIException

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

def get_book_details_seq(isbn):
	"""Get book details using Google Books API (sequentially)"""
	url = GOOGLE_BOOKS_URL + isbn
	response = None
	
	# querying the GoogleBooks API
	with requests.Session() as session:
		try:
			response = session.get(url)
			response.raise_for_status()
		except HTTPError as http_err:
			print(f"HTTP error occurred: {http_err}")
		except Exception as err:
			print(f"An error ocurred: {err}")
		response_json = response.json()
		items = response_json.get("items", [{}])[0]
		
		# if no items then retuen None
		if items == None:
			print('Invalid ISBN number')
			return None
		else:
			volume_info = items.get("volumeInfo", {})
			title = volume_info.get("title", None)
			author = volume_info.get("authors", None)
			
			return (title, author)

# custom exception class to raise the error of book not found when GoogleBooks API 
# does not vaidate the ISBN number passed 
class BookNotFound(APIException):
    status_code = 400
    default_detail = "Unable to find the book in Google Books API."
    default_code = "Bad_ISBN_number"


