import django_filters as filters

from books.models import Book


class BookFilter(filters.FilterSet):
    """ Book object filter class. """
    authors__first_name = filters.CharFilter(
        lookup_expr='iexact', label="Author's first name")
    authors__second_name = filters.CharFilter(
        lookup_expr='icontains', label="Author's other names")
    authors__last_name = filters.CharFilter(
        lookup_expr='iexact', label="Author's last name")
    publication_year = filters.RangeFilter(label="Publication year range")

    class Meta:
        model = Book
        fields = {
            'title': ['iexact', 'icontains'],
            'language': ['exact'],
        }
