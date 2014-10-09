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
	(input_array, data_source) = argument_validation(request)
	
	if input_array == None:
		return data_source
	
	#I need to make parallel requests for every element in the input array with a data source
	data_pluggin = pluggin_factory.get_data_pluggin(data_source)

	#img = data_pluggin.get_first_image(input_array[0])
	img_list = []
	error_list = []
	for species in input_array:
		result = data_pluggin.get_first_image(species)

		#if an error happened and it was the first error received
		if (result == constants.NO_SPECIES_BY_PROVIDED_NAME 
			or result == constants.NO_IMAGES_FOR_SPECIES
			or result == constants.ERROR):
			error_list.append((species, result)) 
		
		else:
			img_list.append((species, result))
	
	return redirection(error_list, img_list, data_source, request, 'treegenerator/result.html')

def pick_results(request):
	(input_array, data_source) = argument_validation(request)
	
	if input_array == None:
		return data_source
	
	#I need to make parallel requests for every element in the input array with a data source
	data_pluggin = pluggin_factory.get_data_pluggin(data_source)
	
	#img = data_pluggin.get_all_images(input_array[0])
	img_list = []
	error_list = []
	for species in input_array:
		result = data_pluggin.get_all_images(species)
		aux = species.replace(' ', '_')
		
		#if an error happened and it was the first error received
		if (result == constants.NO_SPECIES_BY_PROVIDED_NAME 
			or result == constants.NO_IMAGES_FOR_SPECIES
			or result == constants.ERROR):
			error_list.append((aux, result)) 
		
		else:
			img_list.append((aux, result))
	
	return redirection(error_list, img_list, data_source, request, 'treegenerator/multiple_results.html')
	
def argument_validation(request):
	input = request.GET.get(constants.INPUT, '')
	if input == '':
		return (None, HttpResponse('There was an error with your request. Go back to the index page and try again'))
	
	#change from unicode to ascii
	input = unicodedata.normalize('NFKD', input).encode('ascii', 'ignore')
	
	#need tree parsing here
	#for now, I am only extracting all the names of the species from the tree
	input_array = input.replace('(', '').replace(')', '').split(',')
	
	i = 0
	while i < len(input_array):
		input_array[i] = input_array[i].strip()
		i = i + 1
		
	data_source = request.GET.get(constants.DATA_SOURCE, '')
	if data_source == '':
		return (None, HttpResponse('There was an error with your request. Go back to the index page and try again'))
	
	return (input_array, data_source)
	
def redirection(error_list, img_list, data_source, request, no_errors_page):
	if not(len(error_list) == 0):
		context = {'input':			constants.INPUT, 
				'data': 			constants.DATA_SOURCE,
				'sources': 			[constants.PHYLOPIC, 
										constants.ENCYCLOPEDIA_OF_LIFE],
				'system_chooses': 	constants.SYSTEM_CHOOSES,
				'user_chooses': 	constants.USER_CHOOSES,
				'errors': 			error_list,
				'data_source':		data_source,
				'no_data':			constants.NO_SPECIES_BY_PROVIDED_NAME,
				'no_img': 			constants.NO_IMAGES_FOR_SPECIES,
				'error': 			constants.ERROR,
				'user_tree':		request.GET.get(constants.INPUT, '')}
				
		return render(request, 'treegenerator/index.html', context)
	else:	
		#The results would need to be in an array. 
		context = {'result':	img_list,
					'data':		data_source}
		return render(request, no_errors_page , context)
