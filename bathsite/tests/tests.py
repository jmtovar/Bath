from django.test import TestCase
from django.test import Client

class Tests(TestCase):
    def setUp(self):
        self.c = Client()

    def ping_tests(self):
        #Ping test
        response = self.c.get('/ping/')
        self.assertEqual(response.status_code, 200)
        
        #Index
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
        
        #Ete test
        response = self.c.get('/test')
        self.assertEqual(response.status_code, 200)
        
        #Phylopic single image
        response = self.c.get('/result/?input=(((Walrus,%20Homo_sapiens)%20(Black_bear,%20Giant_panda)),%20(fox))&data_source=Phylopic')
        self.assertEqual(response.status_code, 200)
        
        #Phylopic multiple image
        response = self.c.get('/multiple_results/?input=(((Walrus,%20Homo_sapiens)%20(Black_bear,%20Giant_panda)),%20(fox))&data_source=Phylopic')
        self.assertEqual(response.status_code, 200)
        
        #EoL single image
        response = self.c.get('/result/?input=(((Walrus,%20Homo_sapiens)%20(Black_bear,%20Giant_panda)),%20(fox))&data_source=Encyclopedia%20of%20life')
        self.assertEqual(response.status_code, 200)
        
        #EoL multiple image
        response = self.c.get('/multiple_results/?input=(((Walrus,%20Homo_sapiens)%20(Black_bear,%20Giant_panda)),%20(fox))&data_source=Encyclopedia%20of%20life')
        self.assertEqual(response.status_code, 200)
        
    def destructive_test(self):
        #Homo sapiens separated by a space instead of a _
        response = self.c.get('/result/?input=(((Walrus,%20Homo sapiens)%20(Black_bear,%20Giant_panda)),%20(fox))&data_source=Phylopic')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find('missing a comma between taxa names') != -1)
        
        #Incorrect Newick tree format
        response = self.c.get('/result/?input=((Walrus,%20Homo_sapiens)%20(Black_bear,%20Giant_panda)),%20(fox))&data_source=Phylopic')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find('structure of the Newick tree') != -1)
        
        #No data source selected
        response = self.c.get('/result/?input=(((Walrus,%20Homo_sapiens)%20(Black_bear,%20Giant_panda)),%20(fox))&data_source=')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find('was an error with your request') != -1)
        
        #Invalid data source
        response = self.c.get('/result/?input=(((Walrus,%20Homo_sapiens)%20(Black_bear,%20Giant_panda)),%20(fox))&data_source=Not_A_Valid_Data_Source')
        self.assertEqual(response.status_code, 500)
        self.assertTrue(response.content.find('Exception at /result/') != -1)
        
        #No Newick tree
        response = self.c.get('/result/?input=&data_source=Phylopic')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find('was an error with your request') != -1)
    
    def regresion_tests(self):
        #Phylopic single image regresion
        response = self.c.get('/result/?input=(((Walrus,%20Homo_sapiens)%20(Black_bear,%20Giant_panda)),%20(fox))&data_source=Phylopic')
        print response.content
        
        
        
        
        
        
        