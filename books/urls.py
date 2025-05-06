from django.urls import path
from .views import AuthorListCreateView, BookListCreateView

urlpatterns = [
    path('authors/', AuthorListCreateView.as_view()),
    path('books/', BookListCreateView.as_view()),
]
