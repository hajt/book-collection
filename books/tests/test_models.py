from django.test import TestCase
from django import db

from books.models import Author, Book, Language


def create_sample_author(first_name='Hans', second_name='Christian', last_name='Andersen'):
    """ Creating sample Author object. """
    defaults = {
        'first_name': first_name,
        'second_name': second_name,
        'last_name': last_name
    }
    return Author.objects.create(**defaults)


def create_sample_language(language='Polish', shortcut='pl'):
    """ Creating sample Language object. """
    defaults = {
        'language': language,
        'shortcut': shortcut
    }
    return Language.objects.create(**defaults)


def create_sample_book(title='Brzydkie kaczątko', publication_year=2008, isbn=9788372783301, page_count=32, cover_link="http://books.google.com/books/content?id=fdmtAAAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api", language=None, authors=None):
    """ Creating sample Book object. """
    defaults = {
        'title': title,
        'publication_year': publication_year,
        'isbn': isbn,
        'page_count': page_count,
        'cover_link': cover_link,
        'language': language
    }
    book = Book.objects.create(**defaults)
    book.authors.add(*authors)
    book.save()
    return book


class AuthorTests(TestCase):

    def test_author_str(self):
        """ Test author string representation. """
        author = create_sample_author()
        self.assertEqual(str(author), "Hans Christian Andersen")


    def test_get_or_create_many(self):
        """ Test get or create many Manager's method. """
        authors = ['Hans Ch. Andersen', 'Henryk Sienkiewicz']
        Author.objects.get_or_create_many(authors)
        author = Author.objects.first()
        self.assertEqual(Author.objects.count(), 2)
        self.assertEqual(author.first_name, 'Hans')
        self.assertEqual(author.second_name, 'Ch.')
        self.assertEqual(author.last_name, 'Andersen')


    def test_unique_constrains(self):
        """ Test class unique_constrains. """
        create_sample_author()
        with self.assertRaises(db.utils.IntegrityError) as cm:
            create_sample_author()
        self.assertEqual(str(cm.exception), "UNIQUE constraint failed: books_author.first_name, books_author.last_name")
        

class LanguageTests(TestCase):

    def test_language_str(self):
        """ Test language string representation. """
        language = create_sample_language()
        self.assertEqual(str(language), "Polish (pl)")


    def test_unique_constrains(self):
        """ Test class unique_constrains. """
        create_sample_language()
        with self.assertRaises(db.utils.IntegrityError) as cm:
            create_sample_language()
        self.assertEqual(str(cm.exception), "UNIQUE constraint failed: books_language.shortcut")
       

class BookTests(TestCase):

    def setUp(self):
        self.author = create_sample_author()
        self.language = create_sample_language()
        
    
    def test_book_str(self):
        """ Test book string representation. """
        book = create_sample_book(language=self.language, authors=[self.author])
        self.assertEqual(str(book), "Brzydkie kaczątko 2008, isbn=9788372783301, pages: 32")


    def test_unique_constrains(self):
        """ Test class unique_constrains. """
        create_sample_book(language=self.language, authors=[self.author])
        with self.assertRaises(db.utils.IntegrityError) as cm:
            create_sample_book(language=self.language, authors=[self.author])
        self.assertEqual(str(cm.exception), "UNIQUE constraint failed: books_book.title, books_book.publication_year, books_book.language_id")
       
