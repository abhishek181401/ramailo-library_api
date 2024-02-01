from datetime import datetime
from rest_framework import serializers
from .models import Book, BookDetail, BorrowedBook
from account.models import User

class UserSerializer(serializers.ModelSerializer):
    #validating email field
    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError("Invalid. Please include '@' in the email address.")
        return value
    # validae if the username is present or not
    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("This username is already in use.Use any other ")
        return value

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'MembershipDate']

class BookSerializer(serializers.ModelSerializer):
    #validating isbn
    def validate_isbn(self, value):
        cleaned_isbn = value.replace('-', '')  # Removing  hyphens
        if not cleaned_isbn.isdigit():
            raise serializers.ValidationError("Invalid ISBN")
        return value

    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'published_date', 'genre']

class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDetail
        fields = ['book', 'number_of_pages', 'publisher', 'language']

class BorrowedBookSerializer(serializers.ModelSerializer):
    def validate_return_date(self, value):
        borrow_date_str = self.initial_data.get('borrow_date')

        # borrow_date not None and is a valid string
        if borrow_date_str:
            borrow_date = datetime.strptime(borrow_date_str, '%Y-%m-%d').date()

            # comparison
            if value and value < borrow_date:
                raise serializers.ValidationError("Return date can't be earlier than borrow date.")

        return value

    class Meta:
        model = BorrowedBook
        fields = ['user', 'book', 'borrow_date', 'return_date']

