from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from orders.models import Order
from listings.models import Listing

class OrderTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.listing = Listing.objects.create(title='Test Listing', description='Test Description', price=100)

    def test_create_order(self):
        order = Order.objects.create(user=self.user, listing=self.listing, reservation_date=timezone.now())
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.listing, self.listing)


class OrderListViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.listing = Listing.objects.create(title='Test Listing', description='Test Description', price=100)
        Order.objects.create(user=self.user, listing=self.listing)

    def test_order_list_view(self):
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_list.html')