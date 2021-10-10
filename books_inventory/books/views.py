from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView
)
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from books.serializers import (
    BookSerializer, BorrowBookSerializer, UserBorrowBookSerializer
)
from books.models import Book, BorrowBook

User = get_user_model()


class BookListView(APIView):
    """
    List all book, or create.

    """
    @swagger_auto_schema(responses={200: BookSerializer(many=True)})
    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    # @swagger_auto_schema(operation_description="description")
    @swagger_auto_schema(responses={201: BookSerializer()})
    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class BookDetailView(RetrieveAPIView):
    """
    Book details.
    """
    permission_classes = (AllowAny,)
    serializer_class = BookSerializer
    queryset = Book.objects.all()



class BorrowBookListView(APIView):
    """
    List all BorrowBook, or create 
    """
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(responses={200: BookSerializer(many=True)})
    def get(self, request, format=None):
        books = BorrowBook.objects.all()
        serializer = BorrowBookSerializer(books, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={201: BookSerializer()})
    def post(self, request, format=None):
        book_id = request.data.get('book', None)
        if book_id is None:
            return Response({"message": "book invalid data"}, status=HTTP_400_BAD_REQUEST)

        book_obj = Book.objects.get_by_id(book_id)
        if book_obj is None:
            return Response({"message": "invalid book data"}, status=HTTP_400_BAD_REQUEST)
  
        serializer = BorrowBookSerializer(data=request.data)
        if serializer.is_valid():
            if book_obj.book_count > 0:
                serializer.save()
                book_obj.book_count -=1
                book_obj.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response({"message": "book not found"}, status=HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST) 


class BorrowBookUserList(APIView):
    """
    Retrieve, User BorrowBook.
    """
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(responses={200: BookSerializer(many=True)})
    def get(self, request, format=None):
        user=self.request.user
        borrow_books = BorrowBook.objects.filter(user=user)
        serializer = UserBorrowBookSerializer(borrow_books, many=True)
        return Response(serializer.data)
