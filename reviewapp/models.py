from django.db import models
from django.core.validators import MaxValueValidator,\
    MinValueValidator,\
    RegexValidator
from dateutil.parser import parse


class Book(models.Model):
    isbn10 = models.CharField(max_length=10,
                              unique=True,
                              validators=[RegexValidator(regex='[0-9]{10}')])
    isbn13 = models.CharField(max_length=13,
                              unique=True,
                              validators=[RegexValidator(regex='[0-9]{13}')])
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=30)
    publisher = models.CharField(max_length=30)
    cover_link = models.URLField()
    genre = models.IntegerField()
    pub_date = models.DateTimeField()
    description = models.TextField()
    look = models.IntegerField(default=1)
    price_standard = models.IntegerField(null=True)

    @staticmethod
    def json_to_book_dict(json_dict):
        field_names = set(field.name for field in Book._meta.get_fields())
        map_json_and_book_keys = {
            'isbn': 'isbn10',
            'pubDate': 'pub_date',
            'cover': 'cover_link',
            'categoryId': 'genre',
            'priceStandard': 'price_standard',
        }
        book_dict = {}
        for k, v in json_dict.items():
            if k in field_names:
                book_dict[k] = v
            if k in map_json_and_book_keys:
                book_key = map_json_and_book_keys[k]
                book_dict[book_key] = v
                if k == 'pubDate':
                    book_dict['pub_date'] = parse(book_dict['pub_date'])

        return book_dict

    def __str__(self):
        return self.title


class BookStore(models.Model):
    NAVERBOOK = 'naverbook'
    KYOBO = 'kyobo'

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
    book = models.OneToOneField(Book, on_delete=models.CASCADE)


class ItemID(models.Model):
    item_id = models.IntegerField(primary_key=True)
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
