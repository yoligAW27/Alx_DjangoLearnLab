from rest_framework import generics, permissions
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# ============================================
# BOOK VIEWS (Using EXACT class names from requirements)
# ============================================

class ListView(generics.ListAPIView):
    """
    ListView for retrieving all Book instances.
    Provides read-only access to all books.
    Accessible to both authenticated and unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class DetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single Book instance by ID.
    Provides read-only access to a specific book.
    Accessible to both authenticated and unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'


class CreateView(generics.CreateAPIView):
    """
    CreateView for adding a new Book instance.
    Includes custom validation from BookSerializer.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Custom method called when creating a new book."""
        serializer.save()


class UpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing Book instance.
    Supports both PUT (full update) and PATCH (partial update) methods.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        """Custom method called when updating a book."""
        serializer.save()


class DeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a Book instance.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        """Custom method called when deleting a book."""
        instance.delete()


# ============================================
# AUTHOR VIEWS (Optional - keep existing if needed)
# ============================================

class AuthorListView(generics.ListAPIView):
    """ListView for retrieving all Author instances."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class AuthorDetailView(generics.RetrieveAPIView):
    """DetailView for retrieving a single Author instance."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'