from django.test import TestCase
from django.test import Client

class Tests(TestCase):
    def setUp(self):
        c = Client()

    def ping_tests(self):
        response = c.get('/ping/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'pong')
        
    def destructive_test(self):
        