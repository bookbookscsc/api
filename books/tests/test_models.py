from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Review

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
