from datetime import date
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Book, BookDetail, BorrowedBook
from account.models import User


class UserAPITests(APITestCase):
    def test_create_user(self):
        url = reverse('list_create_users')
        data = {'username': 'testuser', 'email': 'test@gmail.com', 'MembershipDate': '2022-01-30', 'password': 'testpassword'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_list_all_users(self):
        url = reverse('list_create_users')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_delete_user(self):
        user = User.objects.create(username='testuser', email='test@example.com', MembershipDate='2022-01-30')
        url = reverse('get_delete_user', args=[user.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

        # deletee
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)


class BookAPITests(APITestCase):
    def test_add_new_book(self):
        url = reverse('list_create_books')
        data = {'title': 'Test Book', 'isbn': '1234567890123', 'published_date': '2022-01-30', 'genre': 'Fiction'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Test Book')

    def test_list_all_books(self):
        url = reverse('list_create_books')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_update_book(self):
        book = Book.objects.create(title='Test Book', isbn='1234567890123', published_date='2022-01-30', genre='xyz')
        url = reverse('get_update_book', args=[book.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

        # Test Update
        data = {'title': 'Updated Book Title', 'isbn': '1234567890123', 'published_date': '2022-01-30', 'genre': 'Fiction'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BorrowedBookAPITests(APITestCase):
    def test_list_create_borrowed_books(self):
        url = reverse('list_create_borrowed_books')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_borrow_book(self):
        user = User.objects.create(username='testuser', email='test@example.com', MembershipDate='2022-01-30')
        book = Book.objects.create(title='Test Book', isbn='1234567890123', published_date='2022-01-30', genre='Fiction')
        book_detail = BookDetail.objects.create(book=book, number_of_pages=100, publisher='Publisher A', language='Spanish')
        url = reverse('list_create_borrowed_books')
        data = {'user': user.id, 'book': book_detail.book.id, 'borrow_date': '2022-01-30'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_update_return_borrowed_book(self):
        user = User.objects.create(username='testuser', email='test@example.com', MembershipDate='2022-01-30')
        book = Book.objects.create(title='Test Book', isbn='1234567890123', published_date='2022-01-30', genre='Fiction')
        book_detail = BookDetail.objects.create(book=book, number_of_pages=100, publisher='Publisher A', language='Spanish')
        borrowed_book = BorrowedBook.objects.create(user=user, book=book_detail.book, borrow_date=date.today())

        url = reverse('get_update_return_borrowed_book', args=[borrowed_book.id])
        data = {'return_date': date.today()}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BorrowedBook.objects.get(id=borrowed_book.id).return_date, date.today())
