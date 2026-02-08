"""
Unit tests for API views in the advanced-api-project.
Tests CRUD operations, filtering, searching, ordering, and permissions.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book
import json


class BookAPITestCase(APITestCase):
    """
    Test case for Book API endpoints.
    Sets up test data and users for comprehensive API testing.
    """
    
    def setUp(self):
        """
        Set up test data before each test method runs.
        Creates test users, authors, and books.
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='J.R.R. Tolkien')
        self.author3 = Author.objects.create(name='George Orwell')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author3
        )
        self.book4 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        
        # API client
        self.client = APIClient()
    
    # ============================================
    # TEST LIST VIEW (GET /api/books/)
    # ============================================
    
    def test_get_all_books(self):
        """
        Test retrieving all books without authentication.
        Should return status 200 and all books.
        """
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # We created 4 books
    
    def test_get_all_books_with_filtering(self):
        """
        Test filtering books by author.
        Should return only books by the specified author.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 books by J.K. Rowling
        for book in response.data:
            self.assertEqual(book['author'], self.author1.id)
    
    def test_get_all_books_with_search(self):
        """
        Test searching books by title.
        Should return books matching the search term.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 Harry Potter books
        for book in response.data:
            self.assertIn('Harry', book['title'])
    
    def test_get_all_books_with_ordering(self):
        """
        Test ordering books by publication year.
        Should return books in specified order.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        
        # Check ordering (oldest first)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [1937, 1949, 1997, 1998])
    
    # ============================================
    # TEST DETAIL VIEW (GET /api/books/<id>/)
    # ============================================
    
    def test_get_single_book(self):
        """
        Test retrieving a single book by ID.
        Should return status 200 and correct book data.
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter and the Philosopher\'s Stone')
        self.assertEqual(response.data['publication_year'], 1997)
        self.assertEqual(response.data['author'], self.author1.id)
    
    def test_get_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist.
        Should return status 404.
        """
        url = reverse('book-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # ============================================
    # TEST CREATE VIEW (POST /api/books/create/)
    # ============================================
    
    def test_create_book_unauthenticated(self):
        """
        Test creating a book without authentication.
        Should return status 401 (Unauthorized).
        """
        url = reverse('book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authenticated(self):
        """
        Test creating a book with authentication.
        Should return status 201 and create the book.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Test Book')
        self.assertEqual(Book.objects.count(), 5)  # Should have 5 books now
    
    def test_create_book_with_future_year(self):
        """
        Test creating a book with a future publication year.
        Should return status 400 due to validation.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Publication year cannot be in the future', str(response.data))
    
    # ============================================
    # TEST UPDATE VIEW (PUT/PATCH /api/books/<id>/update/)
    # ============================================
    
    def test_update_book_unauthenticated(self):
        """
        Test updating a book without authentication.
        Should return status 401.
        """
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_book_authenticated(self):
        """
        Test updating a book with authentication.
        Should return status 200 and update the book.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Updated Harry Potter Title',
            'publication_year': 1998,
            'author': self.author1.id
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Harry Potter Title')
        
        # Verify the update in database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Harry Potter Title')
    
    # ============================================
    # TEST DELETE VIEW (DELETE /api/books/<id>/delete/)
    # ============================================
    
    def test_delete_book_unauthenticated(self):
        """
        Test deleting a book without authentication.
        Should return status 401.
        """
        url = reverse('book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 4)  # Book should not be deleted
    
    def test_delete_book_authenticated(self):
        """
        Test deleting a book with authentication.
        Should return status 204 and delete the book.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 3)  # Should have 3 books now
    
    # ============================================
    # TEST COMBINED FILTERING, SEARCHING, ORDERING
    # ============================================
    
    def test_combined_filter_search_order(self):
        """
        Test combining filtering, searching, and ordering.
        Should return correctly filtered, searched, and ordered results.
        """
        url = reverse('book-list')
        params = {
            'author': self.author1.id,
            'search': 'harry',
            'ordering': '-publication_year'  # Newest first
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 Harry Potter books by Rowling
        
        # Check ordering (newest first)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [1998, 1997])


class AuthorAPITestCase(APITestCase):
    """
    Test case for Author API endpoints.
    """
    
    def setUp(self):
        """Set up test data for author tests."""
        self.author1 = Author.objects.create(name='Test Author 1')
        self.author2 = Author.objects.create(name='Test Author 2')
        
        # Create books for authors
        Book.objects.create(
            title='Book 1',
            publication_year=2000,
            author=self.author1
        )
        Book.objects.create(
            title='Book 2',
            publication_year=2001,
            author=self.author1
        )
        
        self.client = APIClient()
    
    def test_get_all_authors(self):
        """Test retrieving all authors."""
        url = reverse('author-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_author_with_books(self):
        """Test retrieving an author with nested books."""
        url = reverse('author-detail', kwargs={'pk': self.author1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author 1')
        self.assertEqual(len(response.data['books']), 2)  