from rest_framework import serializers
from .models import BookStore, Book, Review


class BookStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookStore
        fields = ('id', 'name')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'title', 'content', 'star')


class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer()
    stores = BookStoreSerializer(many=True)

    class Meta:
        model = Book
        fields = ('id', 'isbn', 'title', 'reviews', 'stores')
