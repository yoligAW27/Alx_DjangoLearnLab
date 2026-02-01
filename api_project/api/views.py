from rest_framework import generics,viewsets,permissions
from .models import Book
from .serializers import BookSerializer
# Create your views here.

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
   

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for full CRUD operations on Book model.
    Permissions:
    - Only authenticated users can access the API (IsAuthenticated).
    - Users must obtain a token via /api-token-auth/ for authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]



