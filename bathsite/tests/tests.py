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
        
    def destructive_tests(self):
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
    
    def regression_tests(self):
        #Phylopic single image regresion
        response = self.c.get('/result/?input=(((Walrus,%20Homo_sapiens)%20(Black_bear,%20Giant_panda)),%20(fox))&data_source=Phylopic')
        self.assertEqual(response.status_code, 200)
        self.assertTrue((response.content.find('c089caae-43ef-4e4e-bf26-973dd4cb65c5') != -1) 
        and (response.content.find('5a5dafa2-6388-43b8-a15a-4fd21cd17594') != -1)
        and (response.content.find('4b1f7a58-8713-4d6e-a130-4c8a1ac2f749') != -1)
        and (response.content.find('20da6c7c-2584-4cee-921b-ebd09384567b') != -1))
        
        
        
        
        
        
        