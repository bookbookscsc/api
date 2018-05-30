from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import Book, BookStore, Review
from ..serializers import ReviewSerializer


class BooksHTTPAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.store = BookStore(name=BookStore.NAVERBOOK)
        self.store.save()

        self.book_pooh = Book(isbn='13394898',
                              title='곰돌이 푸, 행복한 일은 매일 있어',
                              genre='essay')
        self.book_pooh.save()
        self.store.books.add(self.book_pooh)

        self.book_sapiens = Book(isbn='9780781',
                                 title='사피엔스',
                                 genre='humanity')
        self.book_sapiens.save()
        self.store.books.add(self.book_sapiens)

        for i in range(1, 20):
            book = self.book_sapiens if i % 2 is 0 else self.book_pooh
            review = Review(store=self.store,
                            book=book,
                            title='너무 재밌다',
                            content='너무 너무 재밌다',
                            star=5)
            review.save()

    def test_get_hot_books(self):
        response = self.client.get(
            reverse('hot_books', args=['a'])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_reviews_by_isbn(self):
        response = self.client.get(
            '/reviews/13394898'
        )
        serializer = ReviewSerializer(Review.objects.filter(book__isbn=13394898),
                                      many=True)
        self.assertEqual(10, len(serializer.data))
        self.assertEqual(response.data, serializer.data)
