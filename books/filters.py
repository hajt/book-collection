import django_filters

from books.models import Book


class BookFilter(django_filters.FilterSet):

    publication_year = django_filters.RangeFilter()

    class Meta:
        model = Book
        fields = {
            'title': ['contains'],
            'authors': ['exact'],
            'language': ['exact'],
            }
