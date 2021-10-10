from datetime import datetime
from rest_framework import serializers
from books.models import Book, BorrowBook



class BookSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=120)
    author = serializers.CharField(required=True, max_length=120)
    book_count = serializers.IntegerField(required=True)

    def validate_book_count(self, book_count):
        if book_count < 1:
            raise serializers.ValidationError("book_count must be greater than 1.")
        return book_count
    
    class Meta:
        model = Book
        fields = (
            'id',
            'name',
            'slug',
            'author',
            'book_count'
        )


class BorrowBookSerializer(serializers.ModelSerializer):

    def validate_date(self, date):
        try:
            date = datetime.strptime(str(date), "%Y-%m-%d").date()
        except ValueError:
            raise serializers.ValidationError(
                _("Incorrect data format, should be YYYY-MM-DD"))
        return date
    
    class Meta:
        model = BorrowBook
        fields = (
            'id',
            'user',
            'book',
            'date'
        )

class UserBorrowBookSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = BorrowBook
        fields = (
            'id',
            'user',
            'book',
            'date'
        )

    def get_book(self, obj):
        return BookSerializer(obj.book).data