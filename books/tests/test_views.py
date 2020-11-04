from unittest.mock import patch
from django.urls import reverse
from django.test import TestCase

from books.models import Author, Book, Language
from books.external_api import ExternalApi
from books.tests.test_models import create_sample_author, create_sample_language, create_sample_book


class AuthorViewTests(TestCase):

    def setUp(self):
        self.author = create_sample_author()

    def test_create_author(self):
        """ Test create author view. """
        data = {
            'first_name': 'Joanne',
            'second_name': 'Kathleen',
            'last_name': 'Rowling'
        }
        self.client.post(reverse('books:author-create'), data)
        exists = Author.objects.filter(first_name=data['first_name']).exists()
        self.assertTrue(exists)

    def test_update_author(self):
        """ Test update author view. """
        author = Author.objects.first()
        data = {
            'first_name': author.first_name,
            'second_name': 'Ch.',
            'last_name': author.last_name
        }
        self.client.post(
            reverse(
                'books:author-edit',
                kwargs={
                    'pk': author.id}),
            data)
        author.refresh_from_db()
        self.assertEqual(author.second_name, 'Ch.')

    def test_delete_author(self):
        """ Test delete author view. """
        author = Author.objects.first()
        self.client.post(
            reverse(
                'books:author-delete',
                kwargs={
                    'pk': author.id}))
        exists = Author.objects.filter(first_name=author.first_name).exists()
        self.assertFalse(exists)


class LanguageViewTests(TestCase):

    def setUp(self):
        self.language = create_sample_language()

    def test_create_language(self):
        """ Test create language view. """
        data = {
            'language': 'English',
            'shortcut': 'en',
        }
        self.client.post(reverse('books:language-create'), data)
        exists = Language.objects.filter(shortcut=data['shortcut']).exists()
        self.assertTrue(exists)

    def test_update_language(self):
        """ Test update language view. """
        language = Language.objects.first()
        data = {
            'language': 'Polski',
            'shortcut': language.shortcut,
        }
        self.client.post(
            reverse(
                'books:language-edit',
                kwargs={
                    'pk': language.id}),
            data)
        language.refresh_from_db()
        self.assertEqual(language.language, 'Polski')

    def test_delete_language(self):
        """ Test delete language view. """
        language = Language.objects.first()
        self.client.post(
            reverse(
                'books:language-delete',
                kwargs={
                    'pk': language.id}))
        exists = Language.objects.filter(shortcut=language.shortcut).exists()
        self.assertFalse(exists)


class BookViewTests(TestCase):

    def setUp(self):
        self.author = create_sample_author()
        self.language = create_sample_language()
        self.book = create_sample_book(
            language=self.language, authors=[
                self.author])

    def test_delete_book(self):
        """ Test delete book view. """
        book = Book.objects.first()
        self.client.post(reverse('books:book-delete', kwargs={'pk': book.id}))
        exists = Book.objects.filter(title=book.title).exists()
        self.assertFalse(exists)


class ApiImportViewTests(TestCase):

    @patch.object(ExternalApi, 'import_books')
    def test_redirect_valid_url(self, mocked_import_books):
        """ Test redirect api import view when valid url. """
        data = {
            'url': 'https://www.googleapis.com/books/v1/volumes?q=Hobbit',
        }
        mocked_import_books.return_value = 0
        response = self.client.post(reverse('books:api-import'), data)
        self.assertRedirects(
            response,
            reverse('books:book-list'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True)
