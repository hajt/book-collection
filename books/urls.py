from django.urls import path

from books.views import (
    BookFilterListView, 
    BookCreateView, 
    BookUpdateView, 
    BookDeleteView, 
    AuthorListView, 
    AuthorCreateView, 
    AuthorUpdateView,
    AuthorDeleteView,
    LanguageListView, 
    LanguageCreateView, 
    LanguageUpdateView,
    LanguageDeleteView,
    api_import
)



urlpatterns = [
    path('book/list/', BookFilterListView.as_view(), name='book-list'),
    path('book/create/', BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/edit/', BookUpdateView.as_view(), name='book-edit'),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('author/list/', AuthorListView.as_view(), name='author-list'),
    path('author/create/', AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/edit/', AuthorUpdateView.as_view(), name='author-edit'),
    path('author/<int:pk>/delete/', AuthorDeleteView.as_view(), name='author-delete'),
    path('language/list/', LanguageListView.as_view(), name='language-list'),
    path('language/create/', LanguageCreateView.as_view(), name='language-create'),
    path('language/<int:pk>/edit/', LanguageUpdateView.as_view(), name='language-edit'),
    path('language/<int:pk>/delete/', LanguageDeleteView.as_view(), name='language-delete'),
    path('import/', api_import, name='api-import')
]