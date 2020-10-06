# -- FILE: features/list_all_books.feature
Feature: List all the books in the user's collection:
		 In order to list, the user should be logged in 
		 and should have records added.

  Scenario: List all if logged in
    Given the user is logged in with books in his/her collection
     When user visits the url /api/v1/bookcollection/
     Then gets all the books returned with response status as 200.

  Scenario: List all if not logged in
    Given the user is not logged in
     When user visits url /api/v1/bookcollection/ 
     Then user gets authentication error