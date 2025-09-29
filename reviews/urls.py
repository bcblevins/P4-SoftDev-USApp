from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/new/', views.create_book, name='create_book'),
    path('book/<int:book_id>/review/new/', views.create_review, name='create_review'), 
    path('search/', views.search_books, name='search_books'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]