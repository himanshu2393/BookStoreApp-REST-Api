# -- FILE: features/add_book.feature
Feature: Deleting a book from the user's collection:
		 In order to delete, the user should be logged in 
		 and ISBN entered should exist in user's collection

  Scenario: User enters correct ISBN and deletes the book
    Given the user is logged in and has the ISBN
     When user enters wrong ISBN 
     Then book will not be deleted from the database from the user's collection 
	 
  Scenario: User enters wrong ISBN that does not exist
    Given the user is logged in and has ISBN
     When user enters correct ISBN 
     Then book will be deleted from the database from the user's collection