from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend       
from .models import Books, ReadingLists, Authors, Generes
from .serializers import BookSerializer, ReadingListSerializer, AuthorSerializer, GenreSerializer
from .permissions import IsOwner, IsAdminOrOwnerOrReadOnly, IsAdminOrReadOnly



class BookViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['genre', 'author', 'language']  # exact match
    search_fields = ['title', 'subtitle', 'author__first_name', 'author__last_name']
    ordering_fields = ['publication_date', 'created_at', 'title'] 
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReadingListViewSet(viewsets.ModelViewSet):
    serializer_class = ReadingListSerializer
    permission_classes = [IsOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['book__title']
    search_fields = ['book__title', 'book__author__first_name', 'book__author__last_name']
    ordering_fields = ['position', 'date_added']
    ordering = ['position']

    def get_queryset(self):
        return ReadingLists.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



class GenreViewSet(viewsets.ModelViewSet):
    queryset = Generes.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]

