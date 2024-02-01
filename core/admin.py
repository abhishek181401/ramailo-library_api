from django.contrib import admin

# Register your models here.
from .models import Book,BookDetail,BorrowedBook

admin.site.site_header = "Ramailo Library Site"

admin.site.register(Book)
admin.site.register(BookDetail)
admin.site.register(BorrowedBook)