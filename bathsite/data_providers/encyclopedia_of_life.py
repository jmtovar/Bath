from data_providers import data_pluggin
from utils import constants
import urllib2
import json

class EncyclopediaOfLifePluggin(data_pluggin.DataPluggin):
        
    def get_first_image_specific_implementation(self, species, index):
        #returns the url of the first image of the species found in the source
        ids = self.get_ids(species)
        if ids == None:
            self.err_list[index] = (species, constants.NO_SPECIES_BY_PROVIDED_NAME)
            return
        else:
            id = ids[0]
            url = 'http://eol.org/api/pages/1.0/' + str(id) + '.json?images=10&videos=0&sounds=0&maps=0&text=0&iucn=false&subjects=overview&licenses=all&details=false&common_names='
            data_pages = json.load(urllib2.urlopen(url))
            pages_list = data_pages['dataObjects']
            
            if len(pages_list) == 0:
                self.err_list[index] = (species, constants.NO_IMAGES_FOR_SPECIES)
                return
            else:
                object_id = pages_list[0]['dataObjectVersionID']
                url = 'http://eol.org/api/data_objects/1.0/' + str(object_id) + '.json'
                
                image_list = (json.load(urllib2.urlopen(url)))['dataObjects']
                
                if len(image_list) == 0:
                    self.err_list[index] = (species, constants.NO_IMAGES_FOR_SPECIES)
                    return
                else:
                    self.img_list[index] = (species, image_list[0]['mediaURL'])
                    return
    
    def get_all_images_specific_implementation(self, species, index):
        ids = self.get_ids(species)
        if ids == None:
            self.err_list[index] = (species, constants.NO_SPECIES_BY_PROVIDED_NAME)
            return
        else:
            data_objects = []
            for id in ids:
                url = 'http://eol.org/api/pages/1.0/' + str(id) + '.json?images=10&videos=0&sounds=0&maps=0&text=0&iucn=false&subjects=overview&licenses=all&details=false&common_names='
                data_pages = (json.load(urllib2.urlopen(url)))['dataObjects']
                for page in data_pages:
                    data_objects.append(page['dataObjectVersionID'])
            
            if len(data_objects) == 0:
                self.err_list[index] = (species, constants.NO_IMAGES_FOR_SPECIES)
                return
            else:
                img_list = []
                for object in data_objects:
                    url = 'http://eol.org/api/data_objects/1.0/' + str(object) + '.json'
                    aux_list = (json.load(urllib2.urlopen(url)))['dataObjects']
                    for elem in aux_list:
                        img_list.append(elem['mediaURL'])
                        
                if len(img_list) == 0:
                    self.err_list[index] = (species, constants.NO_IMAGES_FOR_SPECIES)
                    return
                else:
                    new_image_list = []
                    
                    #borrar repetidos
                    for i in img_list:
                        if i not in new_image_list:
                            new_image_list.append(i)
                    
                    self.img_list[index] = (species, species.replace(' ', '_'), new_image_list)
                    return
        
    def get_ids(self, species):
        species = species.replace(' ', '+')
        url = 'http://eol.org/api/search/1.0.json?q=' + species + '&page=1&exact=true'
        
        json_id = json.load(urllib2.urlopen(url))
        result_list = json_id['results']
        ids = []
        for result in result_list:
            ids.append(result['id'])
            
        if len(ids) == 0:
            return None
        else:
            return ids
        