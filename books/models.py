from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class BookStore(models.Model):
    name = models.CharField(max_length=20)


class Book(models.Model):
    store = models.ManyToManyField(BookStore)
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=120)


class Review(models.Model):
    store = models.ForeignKey(BookStore,
                              on_delete=models.CASCADE)
    book = models.ForeignKey(Book,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(default="")
    star = models.IntegerField(default=5,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(5)])


