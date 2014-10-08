from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from utils import constants
from data_providers import pluggin_factory
import unicodedata

def index(request):
	context = {'input': constants.INPUT, 
				'data': constants.DATA_SOURCE,
				'sources': [constants.PHYLOPIC, 
					constants.ENCYCLOPEDIA_OF_LIFE],
				'system_chooses': constants.SYSTEM_CHOOSES,
				'user_chooses': constants.USER_CHOOSES}
	return render(request, 'treegenerator/index.html', context)

def result(request):
	input = request.GET.get(constants.INPUT, '')
	if input == '':
		return HttpResponse('There was an error with your request. Go back to the index page and try again')
	
	#change from unicode to ascii
	input = unicodedata.normalize('NFKD', input).encode('ascii', 'ignore')
	
	data_source = request.GET.get(constants.DATA_SOURCE, '')
	if data_source == '':
		data_source = pluggin_factory.DEFAULT
	
	#need tree parsing here
	#for now, I am only extracting all the names of the species from the tree
	input_array = input.replace('(', '').replace(')', '').split(',')
	
	#I need to make parallel requests for every element in the input array with a data source
	data_pluggin = pluggin_factory.get_data_pluggin(data_source)
	
	#img = data_pluggin.get_first_image(input_array[0])
	img_list = []
	for species in input_array:
		aux = (species, data_pluggin.get_first_image(species))
		print aux[0], aux[1]
		img_list.append(aux)
		
	#The results would need to be in an array. 
	context = {'result':	img_list,
				'data':		data_source,
				'no_data':	constants.NO_SPECIES_BY_PROVIDED_NAME,
				'no_img': 	constants.NO_IMAGES_FOR_SPECIES,
				'error': 	constants.ERROR}
	
	return render(request, 'treegenerator/result.html' , context)

def pick_results(request):
	input = request.GET.get(constants.INPUT, '')
	if input == '':
		return HttpResponse('There was an error with your request. Go back to the index page and try again')
	
	#change from unicode to ascii
	input = unicodedata.normalize('NFKD', input).encode('ascii', 'ignore')
	
	data_source = request.GET.get(constants.DATA_SOURCE, '')
	if data_source == '':
		data_source = pluggin_factory.DEFAULT
	
	#need tree parsing here
	#for now, I am only extracting all the names of the species from the tree
	input_array = input.replace('(', '').replace(')', '').split(',')
	
	#I need to make parallel requests for every element in the input array with a data source
	data_pluggin = pluggin_factory.get_data_pluggin(data_source)
	
	#img = data_pluggin.get_all_images(input_array[0])
	img_list = []
	for species in input_array:
		aux = (species, data_pluggin.get_all_images(species))
		print aux[0], aux[1]
		img_list.append(aux)
		
	#The results would need to be in an array. 
	context = {'result':	img_list,
				'data':		data_source,
				'no_data':	constants.NO_SPECIES_BY_PROVIDED_NAME,
				'no_img': 	constants.NO_IMAGES_FOR_SPECIES,
				'error': 	constants.ERROR}
	
	return render(request, 'treegenerator/multiple_results.html' , context)
	