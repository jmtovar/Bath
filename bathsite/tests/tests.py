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
        #Homo sapiens separated by a space instead of a _
        response = c.get('/result/?input=(((Walrus,%20Homo sapiens)%20(Black_bear,%20Giant_panda)),%20(fox))&data_source=Phylopic')
        
        #Incorrect Newick tree format
        response = c.get('/result/?input=((Walrus,%20Homo_sapiens)%20(Black_bear,%20Giant_panda)),%20(fox))&data_source=Phylopic')
        
        #No data source selected
        response = c.get('/result/?input=(((Walrus,%20Homo_sapiens)%20(Black_bear,%20Giant_panda)),%20(fox))&data_source=')
        
        #Invalid data source
        response = c.get('/result/?input=(((Walrus,%20Homo_sapiens)%20(Black_bear,%20Giant_panda)),%20(fox))&data_source=Not_A_Valid_Data_Source')
        
        #No Newick tree
        response = c.get('/result/?input=&data_source=Phylopic')