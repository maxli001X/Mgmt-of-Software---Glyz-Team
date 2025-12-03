from django.test import TestCase, Client
from django.urls import reverse
from .models import ABTestLog

class AnalyticsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/972b69d/'
        self.click_url = reverse('analytics:ab_test_click')

    def test_ab_test_view_status(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Furui Guan")
        self.assertContains(response, "Yichen Li")
        self.assertContains(response, "Yilun Yang")
        self.assertContains(response, "Aozuo Zheng")

    def test_ab_test_view_creates_log(self):
        initial_count = ABTestLog.objects.count()
        self.client.get(self.url)
        self.assertEqual(ABTestLog.objects.count(), initial_count + 1)
        log = ABTestLog.objects.last()
        self.assertEqual(log.event_type, 'view')
        self.assertIn(log.variant, ['A', 'B'])

    def test_ab_test_click_creates_log(self):
        # First visit the page to set the session variant
        self.client.get(self.url)
        
        initial_count = ABTestLog.objects.count()
        response = self.client.post(self.click_url)
        self.assertEqual(response.status_code, 200)
        
        # Should have 1 more log (the click)
        self.assertEqual(ABTestLog.objects.count(), initial_count + 1)
        log = ABTestLog.objects.last()
        self.assertEqual(log.event_type, 'click')

    def test_ab_test_click_without_session(self):
        # Direct post without visiting page first
        response = self.client.post(self.click_url)
        self.assertEqual(response.status_code, 400)

    def test_ab_test_duplicate_click(self):
        # First visit to set session
        self.client.get(self.url)
        
        # First click - should succeed
        response1 = self.client.post(self.click_url)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.json()['status'], 'success')
        
        # Second click - should fail/return error
        response2 = self.client.post(self.click_url)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.json()['status'], 'error')
        self.assertEqual(response2.json()['message'], 'Already clicked')
        
        # Count should only increase by 1 (view + 1 click)
        # View = 1, Click 1 = 1, Click 2 = 0
        # Total logs for this session should be 2
        self.assertEqual(ABTestLog.objects.count(), 2)
