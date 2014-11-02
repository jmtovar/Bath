import abc
import threading

class DataPluggin(object):
    __metaclass__=abc.ABCMeta

    def __init__(self):
        self.img_list = dict()
        self.err_list = dict()
    
    def get_first_image(self, species):
        self.get_first_image_specific_implementation(species)
    
    @abc.abstractmethod
    def get_first_image_specific_implementation(self, species):
        #returns the url of the first image of the species found in the source
        pass

    def get_all_images(self, species):
        self.get_first_image_specific_implementation(species)
    
    @abc.abstractmethod
    def get_all_images_specific_implementation(self, species):
        #returns a list of all the urls for the species found in the source
        pass

class GetImagesThread(threading.Thread):

    def __init__(self, images, errors, lock, queue, id=0):
        """
        :param images: Dictionary for the species->urls.
        :param errors: Dictionary for the species->errors.
        :param lock: Lock to access the dictionaries in the threads.
        :param queue: Queue with the species to be processed.
        :param id: id of the thread in the thread group.
        """
        super(GetImagesThread, self).__init__()
        self.images = images
        self.errors = errors
        self.lock = lock
        self.queue = queue
        self.id = id

