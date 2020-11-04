from django_filters import rest_framework as filters

from books.models import Book


class BookFilter(filters.FilterSet):
    """ Book object filter class. """
    authors__first_name = filters.CharFilter(lookup_expr='iexact')
    authors__second_name = filters.CharFilter(lookup_expr='icontains')
    authors__last_name = filters.CharFilter(lookup_expr='iexact')
    language__shortcut = filters.CharFilter(lookup_expr='iexact')
    publication_year = filters.RangeFilter()

    class Meta:
        model = Book
        fields = {
            'title': ['iexact', 'contains'],
        }
