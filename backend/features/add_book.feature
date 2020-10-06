# -- FILE: features/add_book.feature
Feature: Adding a book in the user's collection:
		 In order to add, the user should be logged in 
		 and ISBN entered should be verified from GoogleBooks API

  Scenario: Wrong ISBN number entered for the book to be saved
    Given the user is logged in and has the book details
     When user enters wrong details & wrong ISBN
     Then GoogleBooks API will reject 
	 And book will not be saved in the database.

  Scenario: Correct ISBN number entered for the book to be saved
    Given the user is logged in and has book details
     When user enters correct ISBN and wrong details 
     Then GoogleBooks API will return title and author to update book details
	 And book will be saved in the database.