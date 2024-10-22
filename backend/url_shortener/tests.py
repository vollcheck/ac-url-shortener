import pytest
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ShortURL


class TestURLShortener(APITestCase):
    def setUp(self):
        """Initialize test data"""
        self.valid_url = "https://www.example.com/very/long/url/that/needs/shortening"
        self.invalid_url = "not-a-valid-url"
        self.shorten_url = reverse('shorten_url')

    def test_create_short_url(self):
        """Test that a valid URL produces a unique short code"""
        data = {'url': self.valid_url}
        response = self.client.post(self.shorten_url, data, format='json')

        # Check response status and structure
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('short_url', response.data)

        # Verify the URL was saved in database
        self.assertTrue(ShortURL.objects.filter(url=self.valid_url).exists())

    def test_short_url_length(self):
        """Verify that the short code length matches the configured length"""
        data = {'url': self.valid_url}
        response = self.client.post(self.shorten_url, data, format='json')

        short_url_endpoint = response.data['short_url'].split('/')[-1]
        expected_length = settings.SHORT_URL_LENGTH

        self.assertEqual(len(short_url_endpoint), expected_length)

    def test_duplicate_url(self):
        """Ensure that submitting the same URL twice returns the same short code"""
        # First submission
        data = {'url': self.valid_url}
        first_response = self.client.post(self.shorten_url, data, format='json')
        first_short_url = first_response.data['short_url']

        # Second submission of the same URL
        second_response = self.client.post(self.shorten_url, data, format='json')
        second_short_url = second_response.data['short_url']

        # Verify both requests return the same short code
        self.assertEqual(first_short_url, second_short_url)

        # Verify only one database entry was created
        self.assertEqual(ShortURL.objects.filter(url=self.valid_url).count(), 1)

    def test_invalid_url(self):
        """Test that invalid URLs are rejected"""
        data = {'url': self.invalid_url}
        response = self.client.post(self.shorten_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_url_validation_patterns(self):
        """Test various URL patterns for validation"""
        test_cases = [
            ('https://example.com', True),
            ('http://example.com', True),
            ('https://example.com/path?param=value', True),
            ('ftp://example.com', True),
            ('just text', False),
            ('http://', False),
        ]

        for url, should_be_valid in test_cases:
            data = {'url': url}
            response = self.client.post(self.shorten_url, data, format='json')

            if should_be_valid:
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertTrue(response.data.get('short_url') is not None)
            else:
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestURLRedirection(APITestCase):
    def setUp(self):
        """Initialize test data"""
        self.short_url = "abc123"
        self.url_mapping = ShortURL.objects.create(
            url="https://www.example.com",
            short_url=self.short_url
        )
        self.redirect_url = reverse('redirect_to_original', kwargs={'short_url': self.short_url})

    def test_successful_redirect(self):
        """Test that accessing a valid short code redirects to the correct URL"""
        response = self.client.get(self.redirect_url)
        visits_count = self.url_mapping.visits_count

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, self.url_mapping.url)
        self.assertEqual(ShortURL.objects.get(short_url=self.short_url).visits_count - visits_count, 1)

    def test_invalid_short_url(self):
        """Test that invalid short codes return a message about invalid URL"""
        invalid_redirect_url = reverse('redirect_to_original', kwargs={'short_url': 'invalid'})
        response = self.client.get(invalid_redirect_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'URL not found'})


class TestShortURLModel(TestCase):
    def test_url_mapping_creation(self):
        """Test URL mapping model creation and retrieval"""
        url_mapping = ShortURL.objects.create(
            url="https://www.example.com",
            short_url="abc123"
        )

        saved_mapping = ShortURL.objects.get(id=url_mapping.id)
        self.assertEqual(saved_mapping.url, "https://www.example.com")
        self.assertEqual(saved_mapping.short_url, "abc123")

    def test_url_mapping_uniqueness(self):
        """Test that duplicate short codes are not allowed"""
        ShortURL.objects.create(
            url="https://www.example.com",
            short_url="abc123"
        )

        with self.assertRaises(Exception):
            ShortURL.objects.create(
                url="https://www.different-example.com",
                short_url="abc123"
            )
