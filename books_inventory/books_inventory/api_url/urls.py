from django.urls import path
from books.views import (
     BookListView,
     BookDetailView,
     BorrowBookListView,
     BorrowBookUserList
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<pk>/', BookDetailView.as_view(), name='book-details'),
    path('borrow-book/', BorrowBookListView.as_view(), name='borrow-book'),
    path('borrow-book-list/', BorrowBookUserList.as_view(), name='borrow-book-list')
]

