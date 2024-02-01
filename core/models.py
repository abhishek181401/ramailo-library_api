from django.db import models

from account.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    published_date = models.DateField()
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
class BookDetail(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, primary_key=True)
    number_of_pages = models.IntegerField()
    publisher = models.CharField(max_length=200)
    language = models.CharField(max_length=200)

    def __str__(self):
        return self.book.title
    
class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

