# Book Collection

*Book Collection is a Web application for managing book collection and with possibility to import books from Google API.*

## Demo

http://hajt.pythonanywhere.com/

## Prerequisites

- **Python** >=**3.7.9** with installed dependencies from **requirements.txt**  

## Local development

1. Pull this repository
2. Install the prerequisites
3. Install Python dependencies:   
`pip install -r requirements.txt`
4. Run Python migrations:  
`python manage.py makemigrations` and    
`python manage.py migrate`  
5. Add Environment Variable:  
`DJANGO_SETTINGS='dev'`   
    **Hint:** *[How to Set Environment Variables in Linux](https://www.serverlab.ca/tutorials/linux/administration-linux/how-to-set-environment-variables-in-linux/)*
6. Run Django server:  
`python manage.py runserver`
7. Add own data or import from Google API

## Available endpoints


List all authors:  
`/collection/author/list/`  
Create author:  
`/collection/author/create/`  
Edit author:  
`/collection/author/<author_id>/edit/`  
Delete author:  
`/collection/author/<author_id>/delete/` 

List all books languages:  
`/collection/language/list/`  
Create language:  
`/collection/language/create/`  
Edit language:  
`/collection/language/<language_id>/edit/`  
Delete language:  
`/collection/language/<language_id>/delete/`


List all books:  
`/collection/book/list/`  
Create book:  
`/collection/book/create/`  
Edit book:  
`/collection/book/<book_id>/edit/`  
Delete book:  
`/collection/book/<book_id>/delete/`   
Import book from API:  
`/collection/import/` 

## API view with query string filters  
List all books:  
`GET /api/books/`  

### Possible filters:
Filter by author first name:  
`?authors__first_name=<name>`  
Filter by author second names:  
`?authors__second_name=<name>`  
Filter by author last name:  
`?authors__last_name=<last_name>`  
Filter by language shortcut:  
`?language__shortcut=<language_shortcut>`  
Filter by publication year greather equal than:  
`?publication_year_min=<year>`  
Filter by publication year less equal than:  
`?publication_year_max=<year>`  
Filter by full title:  
`?title=<title>`  
Filter by title contains:  
`?title__contains=<title>`  

*Example request:*  
`GET /api/books/?authors__first_name=Hans&language__shortcut=pl&publication_year_min=2012&title__contains=szaty`