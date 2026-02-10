from django.test import TestCase
from .models import Author, Book

class AuthorModelTest(TestCase):
    def test_author_creation(self):
        author = Author.objects.create(name="Test Author")
        self.assertEqual(str(author), "Test Author")