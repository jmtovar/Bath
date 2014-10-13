from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from utils import constants
from data_providers import pluggin_factory
from biowrapper.phylogeny import NewickTree
from Bio.Phylo.NewickIO import NewickError

def index(request):
    context = {'input': constants.INPUT, 
                'data': constants.DATA_SOURCE,
                'sources': [pluggin_factory.PHYLOPIC, 
                    pluggin_factory.ENCYCLOPEDIA_OF_LIFE]}
    return render(request, 'treegenerator/index.html', context)

def result(request):
    input = request.GET.get(constants.INPUT, '')
    if input == '':
        return HttpResponse('There was an error with your request. Go back to the index page and try again')
    
    data_source = request.GET.get(constants.DATA_SOURCE, '')
    if data_source == '':
        data_source = pluggin_factory.DEFAULT

    #Parses and should validate the tree. Will also have more functions if needed.
    try :
        nTree = NewickTree(input)
    except NewickError as e :
        return HttpResponse("There is a problem with the structure of the Newick tree.")
    #need tree parsing here
    #for now, I am only extracting all the names of the species from the tree
    input_array = nTree.getSpeciesNames() 
    
    #I need to make parallel requests for every element in the input array with a data source
    data_pluggin = pluggin_factory.get_data_pluggin(data_source)
    
    #Just testing if the data_source works for the first species
    img = data_pluggin.get_first_image(input_array[1])
    
    #The results would need to be in an array. 
    context = {'result': [img],
                'data': data_source}
    
    return render(request, 'treegenerator/result.html' , context)
