from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models.constraints import UniqueConstraint


class Author(models.Model):
    """ Authors model class. """
    firstname = models.CharField(max_length=50)
    secondname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=50)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['firstname', 'lastname'], name='unique_author')
        ]


    def __str__(self):
        return f"{self.firstname} {self.secondname} {self.lastname}"

    def __repr__(self):
        return f"<Author(firstname='{self.firstname}', secondname='{self.secondname}', lastname='{self.lastname}')>"


class Book(models.Model):
    """ Books model class. """
    title = models.CharField(max_length=150)
    pub_year = models.PositiveIntegerField(validators=[MaxValueValidator(2099)])
    page_count = models.PositiveIntegerField(null=True, blank=True)
    cover_link = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=50)

    author = models.ForeignKey(Author, related_name='books', on_delete=models.PROTECT)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['title', 'pub_year', 'language', 'author'], name='unique_book')
        ]


    def __str__(self):
        return f"{self.title} {self.pub_year}, pages: {self.page_count}, language: '{self.language}'"

    def __repr__(self):
        return f"<Book(title='{self.title}', pub_year='{self.pub_year}', page_count='{self.page_count}', cover_link='{self.cover_link}', language='{self.language}')>"

   
class IsbnNumber(models.Model):
    """ ISBN numbers model class. """
    isbn_core = models.CharField(max_length=13)
    isbn_10 = models.CharField(max_length=10, null=True, blank=True)
    isbn_13 = models.CharField(max_length=13, null=True, blank=True)

    book = models.OneToOneField(Book, on_delete=models.CASCADE)


    def __str__(self):
        return f"ISBN_10: {self.isbn_10}, ISBN_13: {self.isbn_13}"

    def __repr__(self):
        return f"<IsbnNumber(isbn_core='{self.isbn_core}, 'isbn_10='{self.isbn_10}', isbn_13='{self.isbn_13}')>"