from rest_framework import serializers

from books.models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    """ Serializer for Author objects. """
    class Meta:
        model = Author
        fields = ['first_name', 'second_name', 'last_name']


class BookSerializer(serializers.ModelSerializer):
    """ Serializer for Book objects. """
    authors = AuthorSerializer(many=True, read_only=True)
    language = serializers.SlugRelatedField(
        slug_field='shortcut', read_only=True)

    class Meta:
        model = Book
        fields = [
            'title',
            'authors',
            'publication_year',
            'language',
            'isbn',
            'page_count',
            'cover_link']
