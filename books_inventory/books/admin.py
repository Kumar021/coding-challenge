from django.contrib import admin

# Register your models here.
from .models import Book, BorrowBook

admin.site.register(Book)
admin.site.register(BorrowBook)