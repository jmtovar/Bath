from data_providers import data_pluggin
from utils import constants
import urllib2
import json
import unicodedata
import threading
import Queue
from urllib2 import URLError

class PhylopicPluggin(data_pluggin.DataPluggin):
    def __init__(self):
        super(PhylopicPluggin, self).__init__()
    
    def get_first_image_specific_implementation(self, species, index):
        #returns the url of the first image of the species found in the source
        lock = threading.Lock()
        queue = Queue.Queue()
        threadNumber = min(10, len(species))

        for i in range(threadNumber) :
            t = GetImageThread(self.img_list, self.err_list, lock, queue, i)
            t.setDaemon(True)
            t.start()

        #populate the queue
        for sp in species :
            queue.put(sp)
        queue.join()
    
    def get_all_images_specific_implementation(self, species, index):
        #TODO move to threads like other method
        #returns a list of all the urls for the species found in the source
        (return_status, json_uid) = self.get_species_uid(species)
        
        if not(return_status):
            self.err_list[index] = (species, json_uid)
            return
        else:
            list = json_uid['result']
            uid_list = []
            for element in list:
                if element['illustrated']:
                    #for some reason the uid comes in unicode type instead of str,
                    #so a conversion is needed
                    uid = element['canonicalName']['uid']
                    uid = unicodedata.normalize('NFKD', uid).encode('ascii', 'ignore')
                    uid_list.append(uid)
                    
            if len(uid_list) == 0:
                self.err_list[index] = (species, constants.NO_IMAGES_FOR_SPECIES)
                return
            else:
                img_list = []
                img_ids = {}
                
                for uid in uid_list:
                    url = 'http://phylopic.org/api/a/name/' + uid + '/images?options=pngFiles'
                    json_img = ''
                    
                    i = 0
                    #Se intenta completar 3 veces la conexion
                    while True:
                        try:
                            json_img = json.load(urllib2.urlopen(url))
                            break
                        except URLError:
                            if i < 3:
                                i = i + 1
                            else:
                                self.err_list[index] = (species, constants.CONNECTION_ERROR)
                                return 
                        except:
                            self.err_list[index] = (species, constants.JSON_ERROR)
                            return
                    
                    if json_img['success']:
                        list = json_img['result']['same']
                        for element in list:
                            
                            inner_list = element['pngFiles']
                            
                            #Phylopic has (as far as I have experimented) 5 resolution sizes for every image, which are enumerated
                            #consecutivly. The format is the same for the 5 images <image_id>.<size>.png
                            #This loop eliminates the repeated images, leaving only the largest one
                            
                            for elem in inner_list:
                                img = unicodedata.normalize('NFKD', elem['url']).encode('ascii', 'ignore')
                                img_key = img.split('.')[0]
                                try:
                                    img_size = int(float(img.split('.')[1]))
                                
                                    if img_ids.has_key(img_key):
                                        if img_ids[img_key] < img_size:
                                            img_ids[img_key] = img_size
                                    else:
                                        img_ids[img_key] = img_size
                                except:
                                    continue
                            
                for k, v in img_ids.items():
                    img_list.append('http://phylopic.org' + k + '.' + str(v) + '.png')
                
                self.img_list[index] = (species, species.replace(' ', '_'), img_list)
                return

class GetImageThread(threading.Thread):
    """
    Thread model to process the species.
    """

    def __init__(self, images, errors, lock, queue, id=0):
        """
        :param images: Dictionary for the species->urls.
        :param errors: Dictionary for the species->errors.
        :param lock: Lock to access the dictionaries in the threads.
        :param queue: Queue with the species to be processed.
        :param id: id of the thread in the thread group.
        """
        threading.Thread.__init__(self)
        self.images = images
        self.errors = errors
        self.lock = lock
        self.queue = queue
        self.id = id

    def get_species_uid(self, species):
        """ Gets the uid for the species from phylopic using the taxon search.
        :param species: Name of the species.
        :return: uid for the species in phylopic.
        """
        buffer = species.replace(' ', '+')

        url = 'http://phylopic.org/api/a/name/search?text=' + buffer + '&options=illustrated';
        try :
            json_uid = json.load(urllib2.urlopen(url))
            if json_uid['success'] and not(len(json_uid['result']) == 0):
                return json_uid
            else:
                return None
        except :
            return None

    def run(self):
        """
        Process the queue and get one image per species. Results are modified directly on the dictionaries provided in
        the thread constructor.
        """
        while True:
            species = self.queue.get()
            self.lock.acquire()
            if not species in self.images : # Species was not processed before.
                self.lock.release()
                print("Starting process for {}".format(species))
                #We need this try to be sure the thread will not die in case of erros while getting data from
                #phylopic
                try :
                    url = None
                    image_url = None
                    json_uid = self.get_species_uid(species)

                    if json_uid is None:
                        print('Error 32')
                        with self.lock:
                            self.errors[species] = constants.NO_SPECIES_BY_PROVIDED_NAME
                            self.images[species] = image_url
                        self.queue.task_done()
                        continue
                    else:
                        element_list = json_uid['result']
                        uids = []

                        for element in element_list:
                            #Check if the element is illustrated
                            if element.has_key('illustrated') and element['illustrated'] == True:
                                #for some reason the uid comes in unicode type instead of str,
                                #so a conversion is needed
                                uid = element['canonicalName']['uid']
                                uid = unicodedata.normalize('NFKD', uid).encode('ascii', 'ignore')
                                uids.append(uid)

                        if len(uids) == 0 : #No images found for species.
                            with self.lock :
                                print('Error 47')
                                self.errors[species] = constants.NO_IMAGES_FOR_SPECIES
                                self.images[species] = image_url
                            self.queue.task_done()
                            continue # To the main while
                        else:
                            for uid in uids :
                                url = 'http://phylopic.org/api/a/name/' + uid + '/images?options=pngFiles'
                                #TODO Try 3 times for connection
                                json_img = json.load(urllib2.urlopen(url))

                                if json_img.has_key('success') and json_img['success'] == True:
                                    element_list = json_img['result']['same']

                                    for element in element_list:
                                        pngFiles = element['pngFiles']
                                        for inner_element in pngFiles:
                                            #for each image there are always versions in different sizes (64, 128, 256, 512 and 1024).
                                            #The first enumerated image is always the size 64 version, so we just replace the image version before the return
                                            print 'Success'
                                            image_url = 'http://phylopic.org' + unicodedata.normalize('NFKD', inner_element['url']).encode('ascii', 'ignore')
                                            break
                                        if not image_url is None :
                                            break
                                if not image_url is None :
                                    break

                            if image_url is None : #No image found, load an error
                                print('Error 47')
                                with self.lock :
                                    self.errors[species] = constants.NO_IMAGES_FOR_SPECIES
                                    self.images[species] = image_url
                                self.queue.task_done()
                                continue # To the main while
                            else :
                                print("Endind task, success {}".format(species))
                                with self.lock:
                                    self.errors[species] = None
                                    self.images[species] = image_url
                                self.queue.task_done()
                                continue # To the main while
                except Exception as ex :
                    with self.lock:
                        self.errors[species] = constants.NO_IMAGES_FOR_SPECIES
                        self.images[species] = image_url #Should be None
                    self.queue.task_done()
            else :
                self.lock_release()
                self.queue.task_done()
