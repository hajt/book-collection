from django.shortcuts import render, redirect
from django_filters.views import FilterView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy

from books.models import Author, Book, Language
from books.filters import BookFilter
from books.forms import ApiImportForm
from books.external_api import ExternalApi


class BookFilterListView(FilterView):
    filterset_class=BookFilter


class BookCreateView(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books:book-list') 


class BookUpdateView(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books:book-list')


class BookDeleteView(DeleteView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books:book-list')


class AuthorListView(ListView):
    model = Author


class AuthorCreateView(CreateView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('books:author-list') 


class AuthorUpdateView(UpdateView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('books:author-list')


class AuthorDeleteView(DeleteView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('books:author-list')


class LanguageListView(ListView):
    model = Language


class LanguageCreateView(CreateView):
    model = Language
    fields = '__all__'
    success_url = reverse_lazy('books:language-list') 


class LanguageUpdateView(UpdateView):
    model = Language
    fields = '__all__'
    success_url = reverse_lazy('books:language-list')


class LanguageDeleteView(DeleteView):
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
