from django.urls import path, reverse_lazy
from django_filters.views import FilterView
from django.views.generic import CreateView


from books.models import Book
from books.filters import BookFilter

urlpatterns = [
    path('book/list/', FilterView.as_view(filterset_class=BookFilter), name='book-list'),
]