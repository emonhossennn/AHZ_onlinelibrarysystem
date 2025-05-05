# serializers placeholder
from rest_framework import serializers
from .models import Book, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), write_only=True, source='author')

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'published', 'author', 'author_id']

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author, _ = Author.objects.get_or_create(**author_data)
        book = Book.objects.create(author=author, **validated_data)
        return book