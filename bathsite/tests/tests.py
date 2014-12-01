from django.test import TestCase
from django.test import Client

class DestructiveTests(TestCase):
    def begin_tests(self):
        c = Client()
        response = c.get('/ping/')
        self.assertEqual(response.status_code, 200)