from rest_framework import serializers
from .models import Books, ReadingLists, Authors, Generes

class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Authors
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'date_of_death', 'full_name']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generes
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Authors.objects.all(), source="author", write_only=True
    )
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Generes.objects.all(), source="genre", write_only=True
    )

    class Meta:
        model = Books
        fields = [
            "id", "title", "subtitle", "book_url", "language", "description",
            "publication_date", "thumbnail", "author", "author_id", "genre", "genre_id"
        ]

class ReadingListSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Books.objects.all(), source="book", write_only=True
    )

    class Meta:
        model = ReadingLists
        fields = ["id", "book", "book_id", "position", "date_added"]
