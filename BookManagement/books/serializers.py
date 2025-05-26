from rest_framework import serializers
from .models import Books, ReadingLists, Authors, Generes

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Authors model.

    This serializer is used to retrieve and display author details, including their full name.

    Attributes:
        full_name (ReadOnlyField): A computed field that returns the full name of the author.

    Meta:
        model (Authors): The model associated with this serializer.
        fields (list): The fields to include in the serialized output.
    """
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Authors
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'date_of_death', 'full_name']

class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for the Generes model.

    This serializer is used to retrieve and display genre details.

    Meta:
        model (Generes): The model associated with this serializer.
        fields (str): All fields of the model are included in the serialized output.
    """
    class Meta:
        model = Generes
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Books model.

    This serializer is used to retrieve, create, and update book details. It includes nested 
    serializers for the author and genre, as well as fields for their IDs for write operations.

    Attributes:
        author (AuthorSerializer): A nested serializer for the author details (read-only).
        genre (GenreSerializer): A nested serializer for the genre details (read-only).
        author_id (PrimaryKeyRelatedField): A field for specifying the author by ID (write-only).
        genre_id (PrimaryKeyRelatedField): A field for specifying the genre by ID (write-only).

    Meta:
        model (Books): The model associated with this serializer.
        fields (list): The fields to include in the serialized output.
    """
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
    """
    Serializer for the ReadingLists model.

    This serializer is used to retrieve, create, and update reading list entries. It includes 
    a nested serializer for the book details and a field for specifying the book by ID.

    Attributes:
        book (BookSerializer): A nested serializer for the book details (read-only).
        book_id (PrimaryKeyRelatedField): A field for specifying the book by ID (write-only).

    Meta:
        model (ReadingLists): The model associated with this serializer.
        fields (list): The fields to include in the serialized output.
    """
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Books.objects.all(), source="book", write_only=True
    )

    class Meta:
        model = ReadingLists
        fields = ["id", "book", "book_id", "position", "date_added"]
