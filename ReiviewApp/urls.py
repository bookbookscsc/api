from django.urls import path
from . import views

urlpatterns = [
    path('hot/<str:genre>', views.get_hot_books, name='hot_books'),
    path('<str:isbn>', views.get_reviews, name='reviews'),
]
