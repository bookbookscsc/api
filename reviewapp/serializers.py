from rest_framework import serializers
from .models import BookStore, Book, Review


class BookStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookStore
        fields = ('id', 'name')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'store', 'book', 'title',
                  'content', 'star',)


class BookSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(source='isbn10')
    cover = serializers.URLField(source='cover_link')
    pubDate = serializers.DateTimeField(source='pub_date')

    class Meta:
        model = Book
        fields = ('id', 'isbn', 'isbn13', 'title', 'author', 'cover', 'look',
                  'genre', 'pubDate', 'description', 'price_standard', 'publisher')
