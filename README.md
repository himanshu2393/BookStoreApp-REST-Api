# BookStoreApp-REST-API
## Description:
BookStoreApp (backend) gives the REST API endpoints for the customers of the bookstore to keep a track of what all books they have read. They can add, delete, and search the books in their collection. This is the backend of the app based on Django Rest Framework and can be dockerized using the Dockerfile (included). This project also involves both Test Driven Development (TDD) and Behaviour Driven Development (BDD) testcases.

## Features Implemented:
- User can register themselves.
- Authorized user, can add books they read in their collection. (Before adding, the book details are verified using GoogleBooks API)
- Can delete one book at a time from their collection.
- Narrow down search for books by the date the books were added in the collection. (Like last 7 days,& so on)
- List all the books in the collection at once.

## Test Cases (TDD & BDD): (only few cases included)
Unit tests covers, how the below mentioned features will respond in the system and behaviour driven test cases are covering different scenarios, the end user might encounter
while using the below mentioned features.

- The files which covers the testcases:
    - unit tests: /bckend/db_api/tests.py
    - bdd tests: /bckend/features

**Features Tested**
  1. **List** book collections (with HttpResponse status code 200) only when the user is logged in or else declare Unauthorized request.
  2. **Add** book in the collection using endpoint request, and verify the record exists in the database for the user.
  3. **Delete** book from the collection using endpoint request, and verify that record should not exists in the database for the user.
  4. **Search** books from the collection using endpoint request by passing the parameter books_added_since last N days, and filter the same from database
     to verify the response is equal.

 To run unit tests & BDD tests: follow the **Build, Test & Execute** section below.

## Build, Test & Execute:
**Requirement: Install Docker** -- In case, you want to run the app in the docker container and make it portable.

-  Clone this repo, to downlaod the codebase.

``` sh
$ git clone https://github.com/himanshu2393/BookStoreApp-REST-Api.git

```
- After docker installation open the bash.
- Change the directory to root folder of the project.
- Build the docker image using Dockerfile.(Installs all the required libraries, including python3.7)

 ``` sh
  $ cd BookStoreApp-REST-Api/
  $ docker build -t backend:latest backend

  ```
  3. Then you can run the container using the image built by exposing the port 8080 (on your host from container). 
  4. You can have any other port like 8000 if 8080 is not free on your machine, but that will require change in the Dockerfile (wherever 8080 is there replace with 8000).
  5. But lets run unit tests and bdd tests before running the app.
  6. Unit testing: (the following command will create and run the docker container followed by the unit testing.)
  
  ``` sh
  $ docker run -v $PWD/backend:/app/backend python manage.py test
  
  ```
  ![unit testing](/images/unit_test.png)
  
  7. BDD testing: (the following command will create and run the docker container followed by the BDD testing.)
  
  ``` sh
  $ docker run -v $PWD/backend:/app/backend python manage.py behave
  
  ```
  ![behave testing](/images/behave_test.png)
  
  8. After testing, let's run the app finally. (Deleting the 2 already created containers (first 2 commands), just in case and then run the app)
  
 ``` sh
  $ docker stop $(docker ps -a -q)
  $ docker rm $(docker ps -a -q)
  $ docker run -v $PWD/backend:/app/backend -p 8080:8080 backend:latest
  
  ```
  5. Thats it!, our app is running now. (if you see...)
  
  ![server running](/images/server_run.png)
  
  6. To access it in the browser, first we need to get our default docker machine IP.
 
 ``` sh
  $ docker-machine ip default
  > 192.168...
  ```
  7. Using this IP, you can access the app running in the container on your host machine. (http://192.168...:8080/api/v1/)
  8. Browsable API URLs:
    - /api/v1/bookcollection/ (logged in users can access, and can list or add books)
    - /api/v1/bookcollection/search/  (logged in users can search or filter on the books, added in last N days)
    - /api/v1/bookcollection/delete_record/ (logged in users can delete a book from the collection)
    - /api/v1/register/ (To register the customer, and only logged out customers can access)
  
  
  
