from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from apps.products.models import Product
from django.core.cache import cache
from unittest.mock import patch

class ProductTests(APITestCase):

    def setUp(self):
        self.product = Product.objects.create(
            asin='B0CGC4PJ3Q',
            name='Test Product',
            price=19.99,
            rating=4.5,
            average_rating=4.4
        )

    def test_retrieve_product_from_db(self):
        url = reverse('product-detail', kwargs={'pk': 'B0CGC4PJ3Q'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['asin'], 'B0CGC4PJ3Q')
        self.assertEqual(response.data['name'], 'Test Product')

    @patch('apps.products.utils.scrape_product_data')
    def test_retrieve_product_from_amazon(self, mock_scrape):
        mock_scrape.return_value = {
            'asin': 'B0CGC4PJ3P',
            'name': 'OtterBox iPhone 15 Pro MAX (Only) Commuter Series Case - CRISP DENIM (Blue), slim & tough, pocket-friendly, with port protection',
            'price': 38.5,
            'rating': 4.6,
            'average_rating': 444
        }
        url = reverse('product-detail', kwargs={'pk': 'B0CGC4PJ3P'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['asin'], 'B0CGC4PJ3P')
        self.assertEqual(response.data['name'], 'OtterBox iPhone 15 Pro MAX (Only) Commuter Series Case - CRISP DENIM (Blue), slim & tough, pocket-friendly, with port protection')
        self.assertTrue(Product.objects.filter(asin='B0CGC4PJ3P').exists())

    @patch('apps.products.utils.scrape_product_data')
    def test_retrieve_product_with_cache(self, mock_scrape):
        mock_scrape.return_value = {
            'asin': 'B0CGC4PJ3P',
            'name': 'OtterBox iPhone 15 Pro MAX (Only) Commuter Series Case - CRISP DENIM (Blue), slim & tough, pocket-friendly, with port protection',
            'price': 38.5,
            'rating': 4.6,
            'average_rating': 444
        }
        cache.set('B0CGC4PJ3P', mock_scrape.return_value)
        url = reverse('product-detail', kwargs={'pk': 'B0CGC4PJ3P'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['asin'], 'B0CGC4PJ3P')
        self.assertEqual(response.data['name'], 'OtterBox iPhone 15 Pro MAX (Only) Commuter Series Case - CRISP DENIM (Blue), slim & tough, pocket-friendly, with port protection')

    def test_retrieve_product_not_found(self):
        url = reverse('product-detail', kwargs={'pk': 'INVALIDASIN'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
