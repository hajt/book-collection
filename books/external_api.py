import requests

from books.models import Author, Book, Language


class ExternalApi:
    """ Class for fetching and import data from external API. """

    def __init__(self, url, headers={'Content-Type':'application/json'}):
        self.url = url
        self.headers = headers


    def import_books(self):
        """ Function which imports books into the database
        and returns the total number of imporeted books. """
        total = 0
        data, error = self._fetch_data()
        if data:
            for item in data['items']:
                created = self._create_book_obj(item['volumeInfo'])
                if created:
                    total += 1
        return total


    def _fetch_data(self):
        """ Function which fetchs data and returns 
        a json and error message if occurs. """ 
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            error = ''
        else:
            data = {}
            error = response.reason
        return data, error


    def _create_book_obj(self, book_data):
        """ Function which gets Book's demandend fields from book data,
        and creates Book object (or gets from database if already exists). """
        title = self._get_title(book_data)
        publication_year = self._get_publication_year(book_data)
        isbn = self._get_isbn(book_data)  
        page_count = self._get_page_count(book_data)
        cover_link = self._get_cover_link(book_data)
        language = self._create_language_obj(book_data)
        authors = self._create_authors_obj(book_data)
        book, created = Book.objects.get_or_create(title=title, publication_year=publication_year, isbn=isbn, page_count=page_count, cover_link=cover_link, language=language)
        if created:
            book.authors.add(*authors)
            book.save()
        return created


    def _get_title(self, book_data):
        """ Function which gets book title and subtitle from passed book data 
        and returns joined title. """        
        title = book_data.get('title')
        subtitle = book_data.get('subtitle')
        if subtitle:
            title = f"{title}: {subtitle}"
        return title


    def _create_authors_obj(self, book_data):
        """ Function which gets list of authors from passed book data,
        returns a list with Author objects. """        
        authors = book_data.get('authors')
        author_objects = Author.objects.get_or_create_many(authors)
        return author_objects


    def _get_page_count(self, book_data):
        """ Function which returns a number of pages from passed book data. """ 
        return book_data.get('pageCount')


    def _get_publication_year(self, book_data):
        """ Function which returns publication year from passed book data. """ 
        year = None
        date = book_data.get('publishedDate')
        if date:
            date = date.split('-')
            if len(date) > 1:
                year = int(date[0])
            else:
                year = int(date.pop())
        return year


    def _create_language_obj(self, book_data):
        """ Function which gets language from passed book data,
        and returns a Language object. """  
        language = book_data.get('language')
        language_object, created = Language.objects.get_or_create(shortcut=language)
        return language_object


    def _get_cover_link(self, book_data):
        """ Function which returns book cover link 
        from passed book data. """ 
        return book_data.get('imageLinks', {}).get('thumbnail')


    def _get_isbn(self, book_data):
        """ Function which returns isbn number from passed book data. """ 
        identyfiers = book_data.get('industryIdentifiers')
        if identyfiers:
            for identyfier in identyfiers:
                if identyfier['type'] == "ISBN_13":
                    isbn = int(identyfier['identifier'])
                    return isbn
