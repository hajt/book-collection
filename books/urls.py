from django.urls import path, reverse_lazy
from django_filters.views import FilterView
from django.views.generic import CreateView, UpdateView, DeleteView


from books.models import Book
from books.filters import BookFilter

urlpatterns = [
    path('book/list/', FilterView.as_view(filterset_class=BookFilter), name='book-list'),
    path('book/create/', CreateView.as_view(model=Book, fields='__all__', success_url=reverse_lazy('books:book-list')), name='book-create'),
    path('book/<int:pk>/edit/', UpdateView.as_view(model=Book, fields='__all__', success_url=reverse_lazy('books:book-list')), name='book-edit'),
    path('book/<int:pk>/delete/', DeleteView.as_view(model=Book, success_url=reverse_lazy('books:book-list')), name='book-delete'),
]