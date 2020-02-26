## TLDR

This application handles login, registration, and allows users to search for, leave reviews, and view info about books.

Search for the title Lowland by Jhumpa Lahiri to see existing reviews from test users or create new reviews and users.

## Summary of Files

### Templates

- base.html - wrapper template contains head tags and link to static css file.
  Other template extend from base template
- index.html - Necessary?
- landing.html - A landing page template when a username is not stored in session data. Anchor tags link to routes login and register links
- login.html - login template form that makes a login post request on submit
- register.html - registration template that contains a form to create a new user and save to database
- search.html - If a username exists in session, the search template is rendered. The template contains a form which includes a text input field and three radio buttons to select the type of data user is searching for. On submit the database is queried for a matching string in the associated field.
- list.html - Search results are rendered with links to individual book pages
- book.html - This template renders individual book data and, if applicable, displays the current user's review of book as well as a list of all reviews book has recieved. If the user has reviewed the book already the user can delete that review. If the user has not reviewed an achor tag is rendered for add_review.html
- add_review.html -

### import.py

This data scraping file is executed in the terminal ( \$python 3 import.py). It reads a csv file containing book data, create connection to database, loops through data and makes an http GET request to the good reads API. If that request returns a status code of 200 (meaning successful), the data is parsed and inserted into appropriate column in the books table.

### application.py

application.py defines routes and their associated functions. These functions query the postgresql database and provide all of the data for template views.

### modules

- helpers.py contains functions that are used in application.py. As the functions for each route began to grow, I decided to break tasks into smaller functions located in external files in order to keep the code cleaner and more readable.

- queries.py contains functions that return postgresql query strings so that route functions. Helps to reuse queries and keep application.py clean

### tests

test_helpers.py and test_queries contain unit tests for helpers.py and queries.py. To run tests make sure you have installed Pytest and run pytest or pytest -vv in root directory of the application

Note--If an error is encountered after installation, ensure the correct version of Werkzeug. Try following steps

## Dependencies

1. Uninstall Werkzeug
   \$ pip3 uninstall Werkzeug
2. Install version 0.16.0
   \$ pip3 install Werkzeug==0.16.0

3. pip install -U MarkupSafe
4. pip install -U pytest for unit tests
