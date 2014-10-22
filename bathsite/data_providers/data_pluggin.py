import abc
import threading

class DataPluggin(object):
    __metaclass__=abc.ABCMeta
    
    img_list = []
    err_list = []
    
    def get_first_image(self, species):
        length = len(species)
        
        self.img_list = [(str(), str()) for i in range(length)]
        self.err_list = [(str(), str()) for i in range(length)]
        threads = [threading.Thread() for i in range(length)]
        
        for i in range(length):
            threads[i].target=self.get_first_image_specific_implementation(species[i], i)
            threads[i].start()
        
        for i in range(length):
            threads[i].join()
    
    @abc.abstractmethod
    def get_first_image_specific_implementation(self, species):
        #returns the url of the first image of the species found in the source
        return
    
    def get_all_images(self, species):
        length = len(species)
        
        self.img_list = [(str(), str(), []) for i in range(length)]
        self.err_list = [(str(), str()) for i in range(length)]
        threads = [threading.Thread() for i in range(length)]
        
        for i in range(length):
            threads[i].target=self.get_all_images_specific_implementation(species[i], i)
            threads[i].start()
        
        for i in range(length):
            threads[i].join()
    
    @abc.abstractmethod
    def get_all_images_specific_implementation(self, species):
        #returns a list of all the urls for the species found in the source
        return
        