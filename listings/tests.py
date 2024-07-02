from django.test import TestCase
from django.urls import reverse
from listings.models import Listing

class ListingTests(TestCase):
    def test_create_listing(self):
        listing = Listing.objects.create(title='Test Listing', description='Test Description', price=100)
        self.assertEqual(listing.title, 'Test Listing')
        self.assertEqual(listing.description, 'Test Description')
        self.assertEqual(listing.price, 100)


class ListingDetailViewTests(TestCase):
    def setUp(self):
        self.listing = Listing.objects.create(title='Test Listing', description='Test Description', price=100)

    def test_listing_detail_view(self):
        response = self.client.get(reverse('listing_detail', args=[self.listing.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/listing_detail.html')