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
							return 'http://phylopic.org' + unicodedata.normalize('NFKD', inner_element['url']).encode('ascii', 'ignore')
					
				else:
					return constants.ERROR
	
	def get_all_images(self, species):
		#returns a list of all the urls for the species found in the source
		json_uid = self.get_species_uid(species)
		
		if json_uid == None:
			return constants.NO_SPECIES_BY_PROVIDED_NAME
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
				return constants.NO_IMAGES_FOR_SPECIES
			else:
				img_list = []
				img_ids = {}
				
				for uid in uid_list:
					url = 'http://phylopic.org/api/a/name/' + uid + '/images?options=pngFiles'
					json_img = json.load(urllib2.urlopen(url))
					
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
				
				return img_list;
		
	def get_species_uid(self, species):
		buffer = species.replace(' ', '+')
				
		url = 'http://phylopic.org/api/a/name/search?text=' + buffer + '&options=illustrated';
		json_uid = json.load(urllib2.urlopen(url))
		
		if json_uid['success'] and not(len(json_uid['result']) == 0):
			return json_uid
		else:
			return None 