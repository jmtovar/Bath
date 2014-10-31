        """
        Parse the tree from the string and return a Tree object.
        :param treeString: String with the tree in Newick format.
        :return: Bio.Phylo.Newick.Tree object with the resulting tree.
        """

INPUT = 'input'
DATA_SOURCE = 'data_source'

def get_parameters():
    '''
    Returns the diferent types of parameters the user has to interact with the system.
    There are the INPUT (tree of species) and the DATA_SOURCE specified by the user to get
    the images from
    :return: List of strings of the parameters
    '''
    return [INPUT, 
            DATA_SOURCE]

PHYLOPIC = 'Phylopic'
ENCYCLOPEDIA_OF_LIFE = 'Encyclopedia of life'

def get_data_pluggins():
    '''
    Returns a list of the different possible data pluggins available to query for images.
    :return: List of string of pluggin names
    '''
    return [PHYLOPIC,
            ENCYCLOPEDIA_OF_LIFE]

NO_SPECIES_BY_PROVIDED_NAME = 'no_species_by_provided_name'
NO_IMAGES_FOR_SPECIES = 'no_images_for_species'
ERROR = 'error'
CONNECTION_ERROR = 'CONNECTION_ERROR'
JSON_ERROR = 'json_error'

def get_possible_errors():
    '''
    Returns a list of possible errors that can be generated within the applicaion
    :return: List of string of possible errors
    '''
    return [NO_SPECIES_BY_PROVIDED_NAME,
            NO_IMAGES_FOR_SPECIES,
            ERROR,
            CONNECTION_ERROR,
            JSON_ERROR]

SYSTEM_CHOOSES = 'system_chooses'
USER_CHOOSES = 'user_chooses'

def get_choosing_forms():
    '''
    
    '''
    return [SYSTEM_CHOOSES,
            USER_CHOOSES]