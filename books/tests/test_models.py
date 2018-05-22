from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Review, Book

from mixer.backend.django import mixer


# Create your tests here.
class ReviewValidationTestCase(TestCase):

    def setUp(self):
        self.review = mixer.blend(Review)

    def test_reviews_should_have_title(self):
        self.review.title = ""
        with self.assertRaises(ValidationError):
            self.review.full_clean()

    def test_reviews_should_have_content(self):
        self.review.content = ""
        with self.assertRaises(ValidationError):
            self.review.full_clean()

    def test_review_title_cannot_exceed_100(self):
        self.review.title = "a" * 101
        with self.assertRaises(ValidationError):
            self.review.full_clean()

    def test_range_of_review_star_should_be_from_0_to_5(self):
        self.review.star = 8
        with self.assertRaises(ValidationError):
            self.review.full_clean()


class BookValidationTestCase(TestCase):

    def setUp(self):
        self.book = mixer.blend(Book)

    def test_isbn_length_should_be_13(self):
        self.book.isbn = '11'
        with self.assertRaises(ValidationError):
            self.book.full_clean()
        self.book.isbn = '1' * 14
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_isbn_should_be_expressed_number(self):
        self.book.isbn = 'a' * 13
        with self.assertRaises(ValidationError):
            self.book.full_clean()
