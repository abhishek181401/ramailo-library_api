from django.urls import path
from .views import (
    list_create_users,
    get_delete_user,
    list_create_books,
    get_update_book,
    list_create_borrowed_books,
    get_update_return_borrowed_book,
    register_user,
    login_user,
)

urlpatterns = [

    # apis for authenticating (bonus part)
    path('register', register_user, name='register_user'),
    path('login', login_user, name='login_user'),
    
    # apis for user
    path('users', list_create_users, name='list_create_users'),
    path('users/<int:user_id>', get_delete_user, name='get_delete_user'),

    # apis for book
    path('books', list_create_books, name='list_create_books'),
    path('books/<int:book_id>', get_update_book, name='get_update_book'),

    # apis  for borrowed books
    path('borrowed-books', list_create_borrowed_books, name='list_create_borrowed_books'),
    path('borrowed-books/<int:borrowed_book_id>', get_update_return_borrowed_book, name='get_update_return_borrowed_book'),
]