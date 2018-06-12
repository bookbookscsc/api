import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime
from django.db.models import F
from ..models import Book, BookStore, Review
from ..serializers import ReviewSerializer


class BooksHTTPAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.store = BookStore(name=BookStore.NAVERBOOK)
        self.store.save()
        date = '2018-01-01'
        self.book_pooh = Book(isbn='13394898',
                              title='곰돌이 푸, 행복한 일은 매일 있어',
                              author='aaaa',
                              cover_link='http://aaa.aaa.aaa',
                              genre=101,
                              pub_date=datetime.strptime(date, '%Y-%m-%d'))
        self.book_pooh.save()
        self.store.books.add(self.book_pooh)

        self.book_sapiens = Book(isbn='9780781',
                                 title='사피엔스',
                                 genre=102,
                                 author='aaaa',
                                 cover_link='http://aaa.aaa.aaa',
                                 pub_date=datetime.strptime(date, '%Y-%m-%d'))
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

    def test_get_trendings(self):
        Book.objects.filter(isbn=self.book_pooh.isbn).update(look=F('look') + 1)
        response = self.client.get(
            reverse('trendings'),
            format='json'
        )
        books_dict = json.loads(response.content, object_hook=Book.json_to_book_dict)
        self.assertEqual(2, len(books_dict))
        self.assertGreater(books_dict[0]['look'], books_dict[1]['look'])

    def test_get_reviews_by_isbn(self):
        response = self.client.get(
            '/reviews/13394898'
        )
        serializer = ReviewSerializer(Review.objects.filter(book__isbn=13394898),
                                      many=True)
        self.assertEqual(10, len(serializer.data))
        self.assertEqual(response.data, serializer.data)
