from django.urls import path
from . import views

urlpatterns = [
    path('trendings', views.get_trendings, name='trendings'),
    path('<str:isbn>', views.get_reviews, name='reviews'),
]
