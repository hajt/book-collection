import unittest
from unittest.mock import patch

from books.external_api import ExternalApi
from books.models import Book
from books.tests.test_models import create_sample_author, create_sample_language, create_sample_book


class TestExternalApi(unittest.TestCase):

    def setUp(self):
        url = "https://www.googleapis.com/books/v1/volumes?q=Hobbit"
        self.external_api = ExternalApi(url)


    @patch('books.external_api.requests.get')
    def test_fetch_data_valid_request(self, mock_requests_get):
        """ Test fetch_data method when valid request. """
        example_data = {
            'example_data': 'data one',
            'example_data2': 'data two',
        }
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = example_data
        data, error = self.external_api._fetch_data()
        self.assertEqual(data, example_data)
        self.assertEqual(error, '')


    @patch('books.external_api.requests.get')
    def test_fetch_data_invalid_request(self, mock_requests_get):
        """ Test fetch_data method when bad request. """
        mock_requests_get.return_value.status_code = 404
        mock_requests_get.return_value.reason = 'Not found'
        data, error = self.external_api._fetch_data()
        self.assertEqual(data, {})
        self.assertEqual(error, 'Not found')


    def test_get_title(self):
        """ Test getting title without subtitle from json data. """
        data = {
            'title': 'Hobbit'
        }
        title = self.external_api._get_title(data)
        self.assertEqual(title, 'Hobbit')


    def test_get_title_with_subtitle(self):
        """ Test getting title with subtitle from json data. """
        data = {
            'title': 'The Hobbit', 
            'subtitle': 'An Unexpected Journey'
        }
        title = self.external_api._get_title(data)
        self.assertEqual(title, 'The Hobbit: An Unexpected Journey')


    def test_create_authors_obj(self):
        """ Test creating authors objects from extracted json data. """
        data = {
            'authors': [
                'Henryk Sienkiewicz',
                'Hans Christian Andersen'
            ]
        }
        authors = self.external_api._create_authors_obj(data)
        self.assertEqual(len(authors), 2)
        self.assertEqual(authors[0].first_name, 'Henryk')
        self.assertEqual(authors[1].second_name, 'Christian')


    def test_get_page_count(self):
        """ Test getting page_count from json data. """
        data = {
            'pageCount': 32
        }
        page_count = self.external_api._get_page_count(data)
        self.assertEqual(page_count, 32)


    def test_get_publication_year_full_date(self):
        """ Test getting publication_year where full date in json data. """
        data = {
            'publishedDate': '2020-10-10'
        }
        publication_year = self.external_api._get_publication_year(data)
        self.assertEqual(publication_year, 2020)

    
    def test_get_publication_year_only_year(self):
        """ Test getting publication_year from json data. """
        data = {
            'publishedDate': '2018'
        }
        publication_year = self.external_api._get_publication_year(data)
        self.assertEqual(publication_year, 2018)

        
    def test_create_language_obj(self):
        """ Test creating language object from extracted json data. """
        data = {
            'language': 'pl'
        }
        language = self.external_api._create_language_obj(data)
        self.assertEqual(language.shortcut, 'pl')


    def test_get_cover_link(self):
        """ Test getting cover_link from json data. """   
        data = {
            'imageLinks': {
                'thumbnail': 'https://cover_link.com' 
            }
        }
        cover_link = self.external_api._get_cover_link(data)
        self.assertEqual(cover_link, 'https://cover_link.com')


    def test_get_isbn(self):
        """ Test getting isbn number from json data. """
        data = {
            'industryIdentifiers': [
                {
                    'type': 'ISBN_13',
                    'identifier': '1234567890123'
                },
            ]
        }
        isbn = self.external_api._get_isbn(data)
        self.assertEqual(isbn, 1234567890123)
    

    def test_get_isbn_no_isbn(self):
        """ Test getting isbn number from json data when no number. """
        data = {
            'industryIdentifiers': [
                {
                    'type': 'other',
                    'identifier': '1234567890123'
                },
            ]
        }
        isbn = self.external_api._get_isbn(data)
        self.assertIsNone(isbn)


    def test_create_book_obj_new_book(self):
        """ Test creating new book object from extracted json data. """
        data = {
            'title': 'Hobbit',
            'authors': [
                'Henryk Sienkiewicz',
            ],
            'pageCount': 32,
            'publishedDate': '2018',
            'language': 'pl',
            'imageLinks': {
                'thumbnail': 'https://cover_link.com' 
            },
            'industryIdentifiers': [
                {
                    'type': 'ISBN_13',
                    'identifier': '1234567890123'
                },
            ],
        }
        created = self.external_api._create_book_obj(data)
        exists = Book.objects.filter(title='Hobbit').exists()
        self.assertTrue(created)
        self.assertTrue(exists)


    def test_create_book_obj_book_exists(self):
        """ Test creating book object from extracted 
        json data when book already exists. """
        language = create_sample_language()
        author = create_sample_author(
            first_name='Adam',
            second_name='',
            last_name='Mickiewicz'
        )
        book = create_sample_book(
            title='Pan Tadeusz',
            cover_link='https://cover_link.com',
            language=language, 
            authors=[author]
        )
        data = {
            'title': 'Pan Tadeusz',
            'authors': [
                'Adam Mickiewicz',
            ],
            'pageCount': 32,
            'publishedDate': '2008',
            'language': 'pl',
            'imageLinks': {
                'thumbnail': 'https://cover_link.com' 
            },
            'industryIdentifiers': [
                {
                    'type': 'ISBN_13',
                    'identifier': '9788372783301'
                },
            ],
        }
        created = self.external_api._create_book_obj(data)
        exists = Book.objects.filter(title='Pan Tadeusz').exists()
        self.assertFalse(created)
        self.assertTrue(exists)


    @patch.object(ExternalApi, '_fetch_data')
    def test_imbort_books_new_book(self, mocked_fetch_data):
        """ Test import new book. """
        data = {
            'items': [
                {
                    'volumeInfo': {
                        'title': 'Dziady',
                        'authors': [
                            'Adam Mickiewicz',
                        ],
                        'pageCount': 300,
                        'publishedDate': '2008',
                        'language': 'pl',
                        'imageLinks': {
                            'thumbnail': 'https://cover_link.com' 
                        },
                        'industryIdentifiers': [
                            {
                                'type': 'ISBN_13',
                                'identifier': '9788372783301'
                            },
                        ],
                    }
                }
            ]
        }
        mocked_fetch_data.return_value = (data, '')
        total = self.external_api.import_books()
        exists = Book.objects.filter(title='Dziady').exists()
        self.assertEqual(total, 1)
        self.assertTrue(exists)