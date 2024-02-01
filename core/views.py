from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from.models import Book,BookDetail,BorrowedBook
from account.models import User
from .serializers import UserSerializer,BookSerializer,BookDetailSerializer,BorrowedBookSerializer

# Create your views here.

#authentication for users (bonus part)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username','')
    password = request.data.get('password','')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)

        # generating and sending token
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    

    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# api for users

@api_view(['GET', 'POST'])
def list_create_users(request):
    try:
        if request.method == 'GET':
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['GET', 'DELETE'])
def get_delete_user(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#api for books
       
@api_view(['GET', 'POST'])
def list_create_books(request):
    try:
        if request.method == 'GET':
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['GET', 'PUT'])
def get_update_book(request, book_id):
    try:
        book = get_object_or_404(Book, id=book_id)

        if request.method == 'GET':
            serializer = BookSerializer(book)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = BookSerializer(instance=book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  

# api for borrowed book
@api_view(['GET', 'POST'])
def list_create_borrowed_books(request):
    try:
        if request.method == 'GET':
            borrowed_books = BorrowedBook.objects.all()
            serializer = BorrowedBookSerializer(borrowed_books, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = BorrowedBookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET', 'PUT'])
def get_update_return_borrowed_book(request, borrowed_book_id):
    try:
        borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_book_id)
        if request.method == 'GET':
            serializer = BorrowedBookSerializer(borrowed_book)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = BorrowedBookSerializer(borrowed_book, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






