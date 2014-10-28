from data_providers import data_pluggin
from utils import constants
import urllib2
import json
import unicodedata

class PhylopicPluggin(data_pluggin.DataPluggin):
    
    def get_first_image_specific_implementation(self, species, index):
        #returns the url of the first image of the species found in the source
        (return_status, json_uid) = self.get_species_uid(species)
        
        if not(return_status):
            self.err_list[index] = (species, json_uid)
            return
        else:
            list = json_uid['result']
            uid = ''
            for element in list:
                if element['illustrated']:
                    #for some reason the uid comes in unicode type instead of str,
                    #so a conversion is needed
                    uid = element['canonicalName']['uid']
                    uid = unicodedata.normalize('NFKD', uid).encode('ascii', 'ignore')
                    break
            
            if uid == '':
                self.err_list[index] = (species, constants.NO_IMAGES_FOR_SPECIES)
                return
            else:
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
                        for inner_element in inner_list:
                            #for each image there are always versions in different sizes (64, 128, 256, 512 and 1024).
                            #The first enumerated image is always the size 64 version, so we just replace the image version before the return
                            self.img_list[index] = (species, 'http://phylopic.org' + unicodedata.normalize('NFKD', inner_element['url']).encode('ascii', 'ignore').replace('.64.png', '.1024.png'))
                            return
                        
                        self.err_list[index] = (species, constants.NO_IMAGES_FOR_SPECIES)
                        return
                    
                    self.err_list[index] = (species, constants.NO_IMAGES_FOR_SPECIES)
                    return
                    
                else:
                    self.err_list[index] = (species, constants.ERROR)
                    return
    
    def get_all_images_specific_implementation(self, species, index):
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
        
    def get_species_uid(self, species):
        buffer = species.replace(' ', '+')
                
        url = 'http://phylopic.org/api/a/name/search?text=' + buffer + '&options=illustrated'
        json_uid = ''
        
        i = 0
        #Se intenta completar 3 veces la conexion
        while True:
            try:
                json_uid = json.load(urllib2.urlopen(url))
                break
            except URLError:
                if i < 3:
                    i = i + 1
                else:
                    return (False, constants.CONNECTION_ERROR)
            except:
                return (False, constants.JSON_ERROR)
        
        if json_uid['success'] and not(len(json_uid['result']) == 0):
            return (True, json_uid)
        else:
            return (False, constants.NO_SPECIES_BY_PROVIDED_NAME) 