from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from books.models import Author, Book, Language
from books.filters import BookFilter
from books.forms import ApiImportForm
from books.external_api import ExternalApi


class BookFilterListView(FilterView):
    """ Book filter list view class. """
    filterset_class = BookFilter


class BookCreateView(CreateView):
    """ Book create view class. """
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books:book-list')


class BookUpdateView(UpdateView):
    """ Book update view class. """
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books:book-list')


class BookDeleteView(DeleteView):
    """ Book delete view class. """
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books:book-list')


class AuthorListView(ListView):
    """ Author list view class. """
    model = Author


class AuthorCreateView(CreateView):
    """ Author create view class. """
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('books:author-list')


class AuthorUpdateView(UpdateView):
    """ Author update view class. """
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('books:author-list')


class AuthorDeleteView(DeleteView):
    """ Author delete view class. """
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('books:author-list')


class LanguageListView(ListView):
    """ Language list view class. """
    model = Language


class LanguageCreateView(CreateView):
    """ Language create view class. """
    model = Language
    fields = '__all__'
    success_url = reverse_lazy('books:language-list')


class LanguageUpdateView(UpdateView):
    """ Language update view class. """
    model = Language
    fields = '__all__'
    success_url = reverse_lazy('books:language-list')


class LanguageDeleteView(DeleteView):
    """ Language delete view class. """
    model = Language
    fields = '__all__'
    success_url = reverse_lazy('books:language-list')


def api_import(request):
    """ View for import data from external API. """
    if request.method == 'POST':
        form = ApiImportForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            external_api = ExternalApi(url)
            total = external_api.import_books()
            return redirect('books:book-list')
    else:
        form = ApiImportForm()
    return render(request, 'books/api_import.html', {'form': form})
