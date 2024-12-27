# Register your models here.
from django.contrib import admin
from .models import Shelf, Book, Author


admin.site.register(Shelf)
admin.site.register(Book)
admin.site.register(Author)
