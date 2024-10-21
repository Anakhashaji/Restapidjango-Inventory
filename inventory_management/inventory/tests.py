from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Item
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken

class InventoryAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        self.item = Item.objects.create(name='Test Item', description='Test Description', quantity=10)
        self.url = reverse('items')

    def test_authentication(self):
        # Test accessing endpoint without authentication
        self.client.credentials()  # Clear credentials
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test accessing endpoint with authentication
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_item(self):
        data = {'name': 'New Item', 'description': 'New Description', 'quantity': 5}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(Item.objects.get(name='New Item').quantity, 5)

    def test_create_duplicate_item(self):
        data = {'name': 'Test Item', 'description': 'Duplicate Item', 'quantity': 5}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Item.objects.count(), 1)  # No new item should be created

    def test_read_item(self):
        url = reverse('item-detail', args=[self.item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Item')
        self.assertEqual(response.data['quantity'], 10)

    def test_update_item(self):
        url = reverse('item-detail', args=[self.item.id])
        data = {'name': 'Updated Item', 'description': 'Updated Description', 'quantity': 15}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Item')
        self.assertEqual(self.item.quantity, 15)

    def test_delete_item(self):
        url = reverse('item-detail', args=[self.item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.count(), 0)

    def test_list_items(self):
        Item.objects.create(name='Second Item', description='Another Description', quantity=20)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_redis_caching(self):
        url = reverse('item-detail', args=[self.item.id])
        
        # First request should cache the item
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        
        # Modify the item directly in the database
        Item.objects.filter(id=self.item.id).update(name='Modified Item')
        
        # Second request should return the cached item
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['name'], 'Test Item')  # Not 'Modified Item'
        
        # Clear the cache
        cache.clear()
        
        # Third request should return the updated item
        response3 = self.client.get(url)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.data['name'], 'Modified Item')

    def test_item_not_found(self):
        url = reverse('item-detail', args=[999])  # Non-existent item
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_update(self):
        url = reverse('item-detail', args=[self.item.id])
        data = {'name': '', 'description': 'Invalid Update', 'quantity': -5}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.item.refresh_from_db()
        self.assertNotEqual(self.item.name, '')
        self.assertNotEqual(self.item.quantity, -5)

    def tearDown(self):
        cache.clear()