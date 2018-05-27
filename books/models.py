from django.db import models
from django.core.validators import MaxValueValidator,\
    MinValueValidator,\
    RegexValidator


class Book(models.Model):
    isbn = models.CharField(max_length=13,
                            unique=True,
                            validators=[RegexValidator(regex='[0-9]{10,13}')])
    title = models.CharField(max_length=120)
    genre = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class BookStore(models.Model):
    name = models.CharField(max_length=20)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name


class Review(models.Model):
    store = models.ForeignKey(BookStore,
                              on_delete=models.CASCADE)
    book = models.ForeignKey(Book,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    star = models.IntegerField(default=5,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(5)])

    def __str__(self):
        return f'store : {self.store.name}, book : {self.book.title}, title : {self.title}'


class BID(models.Model):
    bid = models.IntegerField(primary_key=True)
    book = models.OneToOneField(Book)


class ItemID(models.Model):
    item_id = models.IntegerField(primary_key=True)
    book = models.OneToOneField(Book)
