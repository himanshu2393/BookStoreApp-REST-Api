# -- FILE: features/search.feature
Feature: Searching the books (added since last 7,14.. days etc.) in the user's collection:
		 In order to search, the user should be logged in 
		 and should enter the number of days (like last 7 days or so) to filter and return the response

  Scenario: User entered the number of days N and does not get records
    Given the user is logged in and has not added any books in last N days
     When user enters the number of days
     Then gets empty records  

  Scenario: User entered the number of days and gets the filtered records
    Given the user is logged in and has books added in last N days
     When user enters number of days 
     Then user gets filtered records

  Scenario: User entered number of days less than min. days (i.e. 1)
    Given the user is logged in and has books in collection
     When user enters number of days as less than 1 
     Then user gets response error bad request.
	 
  Scenario: User entered number of days more than max. days (i.e. 30)
    Given the user is logged in and has books added in collection
     When user enters number of days more than 30 
     Then user gets error bad request.