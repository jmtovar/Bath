from data_providers import data_pluggin
from utils import constants
import urllib2
import json
import unicodedata

class PhylopicPluggin(data_pluggin.DataPluggin):
	
	def get_first_image(self, species):
		#returns the url of the first image of the species found in the source
		json_uid = self.get_species_uid(species)
		
		if json_uid == None:
			return constants.NO_SPECIES_BY_PROVIDED_NAME
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
				return constants.NO_IMAGES_FOR_SPECIES
			else:
				url = 'http://phylopic.org/api/a/name/' + uid + '/images?options=pngFiles'
				json_img = json.load(urllib2.urlopen(url))
				
				if json_img['success']:
					list = json_img['result']['same']
					for element in list:
						
						inner_list = element['pngFiles']
						for inner_element in inner_list:
							return 'http://phylopic.org/' + inner_element['url']
					
				else:
					return constants.ERROR
	
	def get_all_images(self, species):
		#returns a list of all the urls for the species found in the source
		json = get_species_uid(species)
		
		return
		
	def get_species_uid(self, species):
		length = len(species)
		buffer = species.replace(' ', '+')
				
		url = 'http://phylopic.org/api/a/name/search?text=' + buffer + '&options=illustrated';
		print url
		json_uid = json.load(urllib2.urlopen(url))
		
		if json_uid['success']:
			return json_uid
		else:
			return None 