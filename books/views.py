from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from rest_framework.response import Response

class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author']

    def get_queryset(self):
        return Book.objects.all()

    def list(self, request, *args, **kwargs):
        cache_key = 'book_list_cache'
        data = cache.get(cache_key)
        if not data:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, timeout=60*30)
        return Response(data)

    def create(self, request, *args, **kwargs):
        cache.delete('book_list_cache')
        return super().create(request, *args, **kwargs)
