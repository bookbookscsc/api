from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer


@api_view(['GET'])
def get_trendings(request):
    books = Book.objects.order_by('-look')[:10]
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_reviews(request, isbn):
    length = len(isbn)
    if length == 10:
        reviews = Review.objects.filter(book__isbn10=isbn)
    else:
        reviews = Review.objects.filter(book__isbn13=isbn)
    bookstore = request.GET.get('bookstore')
    if bookstore is not None:
        reviews = reviews.filter(store=bookstore)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)
