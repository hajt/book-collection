from rest_framework import viewsets, mixins

from books.models import Book
from api.serializers import BookSerializer
from api.filters import BookFilter


class BookViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """ Viewset for list books. """
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filterset_class = BookFilter
