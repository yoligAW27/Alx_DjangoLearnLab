from django.test import TestCase

# Create your tests here.
"""
Test module for API endpoints.
This file imports tests from test_views.py to maintain compatibility.
"""
from .test_views import BookAPITestCase, AuthorAPITestCase

# This ensures Django's test runner can find the tests
__all__ = ['BookAPITestCase', 'AuthorAPITestCase']