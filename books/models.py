from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models.constraints import UniqueConstraint


class Author(models.Model):
    """ Authors model class. """
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=50)


    class Meta:
        constraints = [
            UniqueConstraint(fields=['first_name', 'last_name'], name='unique_author')
        ]


    def __str__(self):
        return f"{self.first_name} {self.second_name} {self.last_name}"

    def __repr__(self):
        return f"<Author(first_name='{self.first_name}', second_name='{self.second_name}', last_name='{self.last_name}')>"


class Language(models.Model):
    """ Languages model class. """
    language = models.CharField(max_length=50)
    shortcut = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.language} ({self.shortcut})"

    def __repr__(self):
        return f"<Language(language='{self.language}', shortcut='{self.shortcut}')>"


class Book(models.Model):
    """ Books model class. """
    title = models.CharField(max_length=150)
    publication_year = models.PositiveIntegerField(validators=[MaxValueValidator(2099)])
    isbn = models.PositiveIntegerField(null=True, blank=True)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    cover_link = models.CharField(max_length=200, null=True, blank=True)

    language = models.ForeignKey(Language, related_name='books', on_delete=models.PROTECT)
    authors = models.ManyToManyField(Author, related_name='books', through='BookAuthor')


    class Meta:
        constraints = [
            UniqueConstraint(fields=['title', 'publication_year', 'language'], name='unique_book')
        ]


    def __str__(self):
        return f"{self.title} {self.publication_year}, pages: {self.page_count}, language: '{self.language}'"

    def __repr__(self):
        return f"<Book(title='{self.title}', publication_year='{self.publication_year}', page_count='{self.page_count}', cover_link='{self.cover_link}', language='{self.language}')>"


class BookAuthor(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)