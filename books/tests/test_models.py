from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Review, Book, BookStore

from mixer.backend.django import mixer


class ValidationTestCase(TestCase):
    def assert_raise_validation_error_in(self, model):
        with self.assertRaises(ValidationError):
            model.full_clean()


# Create your tests here.
class ReviewValidationTestCase(ValidationTestCase):

    def setUp(self):
        self.review = mixer.blend(Review)

    def test_reviews_should_have_title(self):
        self.review.title = ""
        self.assert_raise_validation_error_in(self.review)

    def test_reviews_should_have_content(self):
        self.review.content = ""
        self.assert_raise_validation_error_in(self.review)

    def test_review_title_cannot_exceed_100(self):
        self.review.title = "a" * 101
        self.assert_raise_validation_error_in(self.review)

    def test_range_of_review_star_should_be_from_0_to_5(self):
        self.review.star = 8
        self.assert_raise_validation_error_in(self.review)


class BookValidationTestCase(ValidationTestCase):

    def setUp(self):
        self.book = mixer.blend(Book)

    def test_book_isbn_length_should_be_13(self):
        self.book.isbn = '11'
        self.assert_raise_validation_error_in(self.book)
        self.book.isbn = '1' * 14
        self.assert_raise_validation_error_in(self.book)

    def test_book_isbn_should_be_expressed_number(self):
        self.book.isbn = 'a' * 13
        self.assert_raise_validation_error_in(self.book)

    def test_book_title_cannot_exceed_120(self):
        self.book.title = 'a' * 121
        self.assert_raise_validation_error_in(self.book)

    def test_book_should_have_title(self):
        self.book.title = ''
        self.assert_raise_validation_error_in(self.book)

    def test_book_genre_cannot_exceed_10(self):
        self.book.genre = 'a' * 12
        self.assert_raise_validation_error_in(self.book)

    def test_book_should_have_a_specific_genre(self):
        self.book.genre = ''
        self.assert_raise_validation_error_in(self.book)


class BookStoreValidationTest(ValidationTestCase):

    def setUp(self):
        self.book_store = mixer.blend(BookStore)

    def test_book_store_name_length_cannot_exceed_20(self):
        self.book_store.name = 'a' * 21
        self.assert_raise_validation_error_in(self.book_store)

    def test_book_store_have_name(self):
        self.book_store.name = ''
        self.assert_raise_validation_error_in(self.book_store)


class ReviewTestCase(TestCase):

    def setUp(self):
        self.review = mixer.blend(Review)

    def test__str__method(self):
        self.assertEqual(str(self.review),
                         f'store : {self.review.store.name},'
                         f' book : {self.review.book.title},'
                         f' title : {self.review.title}')


class BookTestCase(TestCase):

    def setUp(self):
        self.book = mixer.blend(Book)

    def test__str__method(self):
        self.assertEqual(str(self.book), self.book.title)


class BookStoreTestCase(TestCase):

    def setUp(self):
        self.book_store = mixer.blend(BookStore)

    def test__str__method(self):
        self.assertEqual(str(self.book_store), self.book_store.name)
