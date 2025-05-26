from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend       
from .models import Books, ReadingLists, Authors, Generes
from .serializers import BookSerializer, ReadingListSerializer, AuthorSerializer, GenreSerializer
from .permissions import IsOwner, IsAdminOrOwnerOrReadOnly, IsAdminOrReadOnly



class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing books.

    This viewset provides CRUD operations for books, including filtering, searching, 
    and ordering. Users can view all books, but only admins or the creator of a book 
    can modify or delete it.

    Attributes:
        queryset (QuerySet): The queryset of all books.
        serializer_class (BookSerializer): The serializer used for book data.
        permission_classes (list): Permissions required to access this viewset.
        filter_backends (list): Backends for filtering, searching, and ordering.
        filterset_fields (list): Fields available for exact match filtering.
        search_fields (list): Fields available for search functionality.
        ordering_fields (list): Fields available for ordering results.
        ordering (list): Default ordering for the queryset.

    Methods:
        perform_create(serializer): Saves the book with the current user as the creator.
    """
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'author', 'language']
    search_fields = ['title', 'subtitle', 'author__first_name', 'author__last_name']
    ordering_fields = ['publication_date', 'created_at', 'title']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """
        Save the book instance with the current user as the creator.

        Args:
            serializer (Serializer): The serializer instance containing validated data.
        """
        serializer.save(created_by=self.request.user)


class ReadingListViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing reading lists.

    This viewset allows users to create, view, update, and delete their reading lists.
    Each user can only access their own reading list.

    Attributes:
        serializer_class (ReadingListSerializer): The serializer used for reading list data.
        permission_classes (list): Permissions required to access this viewset.
        filter_backends (list): Backends for filtering, searching, and ordering.
        filterset_fields (list): Fields available for exact match filtering.
        search_fields (list): Fields available for search functionality.
        ordering_fields (list): Fields available for ordering results.
        ordering (list): Default ordering for the queryset.

    Methods:
        get_queryset(): Returns the reading list for the current user.
        perform_create(serializer): Saves the reading list with the current user as the owner.
    """
    serializer_class = ReadingListSerializer
    permission_classes = [IsOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['book__title']
    search_fields = ['book__title', 'book__author__first_name', 'book__author__last_name']
    ordering_fields = ['position', 'date_added']
    ordering = ['position']

    def get_queryset(self):
        """
        Retrieve the reading list for the authenticated user.

        Returns:
            QuerySet: The reading list for the current user.
        """
        return ReadingLists.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Save the reading list instance with the current user as the owner.

        Args:
            serializer (Serializer): The serializer instance containing validated data.
        """
        serializer.save(user=self.request.user)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing authors.

    This viewset provides CRUD operations for authors. Only admins or the user who 
    created an author can modify or delete it. All users can view authors.

    Attributes:
        queryset (QuerySet): The queryset of all authors.
        serializer_class (AuthorSerializer): The serializer used for author data.
        permission_classes (list): Permissions required to access this viewset.

    Methods:
        perform_create(serializer): Saves the author with the current user as the creator.
    """
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def perform_create(self, serializer):
        """
        Save the author instance with the current user as the creator.

        Args:
            serializer (Serializer): The serializer instance containing validated data.
        """
        serializer.save(created_by=self.request.user)


class GenreViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing genres.

    This viewset provides CRUD operations for genres. Only admins can create, update, 
    or delete genres. All users can view genres.

    Attributes:
        queryset (QuerySet): The queryset of all genres.
        serializer_class (GenreSerializer): The serializer used for genre data.
        permission_classes (list): Permissions required to access this viewset.
    """
    queryset = Generes.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]

