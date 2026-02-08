from django.urls import path
from .views import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
    AuthorListView, AuthorDetailView
)

urlpatterns = [
    # Book CRUD endpoints with exact view names
    path('books/', ListView.as_view(), name='book-list'),
    path('books/create/', CreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', DetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', UpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', DeleteView.as_view(), name='book-delete'),
    
    # Author endpoints (optional)
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]