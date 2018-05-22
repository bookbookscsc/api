from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Review, Book

from mixer.backend.django import mixer


class ValidationTestCase(TestCase):
    def validation_check(self, model):
        with self.assertRaises(ValidationError):
            model.full_clean()


# Create your tests here.
class ReviewValidationTestCase(ValidationTestCase):

    def setUp(self):
        self.review = mixer.blend(Review)

    def test_reviews_should_have_title(self):
        self.review.title = ""
        self.validation_check(self.review)

    def test_reviews_should_have_content(self):
        self.review.content = ""
        self.validation_check(self.review)

    def test_review_title_cannot_exceed_100(self):
        self.review.title = "a" * 101
        self.validation_check(self.review)

    def test_range_of_review_star_should_be_from_0_to_5(self):
        self.review.star = 8
        self.validation_check(self.review)


class BookValidationTestCase(ValidationTestCase):

    def setUp(self):
        self.book = mixer.blend(Book)

    def test_isbn_length_should_be_13(self):
        self.book.isbn = '11'
        self.validation_check(self.book)
        self.book.isbn = '1' * 14
        self.validation_check(self.book)

    def test_isbn_should_be_expressed_number(self):
        self.book.isbn = 'a' * 13
        self.validation_check(self.book)

    def test_book_title_cannot_exceed_120(self):
        self.book.title = 'a' * 121
        self.validation_check(self.book)

    def test_book_should_have_title(self):
        self.book.title = ''
        self.validation_check(self.book)
