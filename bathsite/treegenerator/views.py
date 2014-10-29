from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from utils import constants
from data_providers import pluggin_factory
import unicodedata
from biowrapper.phylogeny import NewickTree
from Bio.Phylo.NewickIO import NewickError
from data_providers.cache import CacheController

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
    
    data_pluggin = pluggin_factory.get_data_pluggin(data_source)
    data_pluggin.get_first_image(input_array)
    
    return redirection(data_pluggin.err_list, data_pluggin.img_list, data_source, request, 'treegenerator/result.html')

def pick_results(request):
    (input_array, data_source) = argument_validation(request)
    
    for i in input_array:
        print i
    
    if input_array == None:
        return data_source
    
    #I need to make parallel requests for every element in the input array with a data source
    data_pluggin = pluggin_factory.get_data_pluggin(data_source)
    cache = CacheController()
    cachedSpecies, input_array = cache.tryCache(input_array, data_source)
    data_pluggin.get_all_images(input_array)
    cache.storeCache(data_pluggin.img_list, data_source)
    
    return redirection(data_pluggin.err_list, data_pluggin.img_list, data_source, request, 'treegenerator/multiple_results.html')
    
def argument_validation(request):
    input = request.GET.get(constants.INPUT, '')
    if input == '':
        return (None, HttpResponse('There was an error with your request. Go back to the index page and try again'))
    
    #change from unicode to ascii
    input = unicodedata.normalize('NFKD', input).encode('ascii', 'ignore')
    
    #Parses and should validate the tree. Will also have more functions if needed.
    try :
        nTree = NewickTree(input)
    except NewickError as e :
        return (None, HttpResponse("There is a problem with the structure of the Newick tree."))
    input_array = [name.strip().replace('_', ' ') for name in nTree.getSpeciesNames()]
    
    data_source = request.GET.get(constants.DATA_SOURCE, '')
    if data_source == '':
        return (None, HttpResponse('There was an error with your request. Go back to the index page and try again'))
    
    return (input_array, data_source)
    
def redirection(error_list, img_list, data_source, request, no_errors_page):
    errors_present = False
    
    for species in  error_list.keys():
        if not error_list[species] is None :
            errors_present = True
            break
    
    if errors_present:
        print 'Errors present'
        context = {'input':            constants.INPUT, 
                'data':             constants.DATA_SOURCE,
                'sources':             [constants.PHYLOPIC, 
                                        constants.ENCYCLOPEDIA_OF_LIFE],
                'system_chooses':     constants.SYSTEM_CHOOSES,
                'user_chooses':     constants.USER_CHOOSES,
                'errors':             error_list,
                'data_source':        data_source,
                'no_data':            constants.NO_SPECIES_BY_PROVIDED_NAME,
                'no_img':             constants.NO_IMAGES_FOR_SPECIES,
                'error':             constants.ERROR,
                'user_tree':        request.GET.get(constants.INPUT, '')}
                
        return render(request, 'treegenerator/index.html', context)
    else:    
        print 'No present errors'

        context = {'result':    img_list,
                    'data':        data_source}
        return render(request, no_errors_page , context)
