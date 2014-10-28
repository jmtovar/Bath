INPUT = 'input'
DATA_SOURCE = 'data_source'

def get_parameters():
    return [INPUT, 
            DATA_SOURCE]

PHYLOPIC = 'Phylopic'
ENCYCLOPEDIA_OF_LIFE = 'Encyclopedia of life'

def get_data_pluggins():
    return [PHYLOPIC,
            ENCYCLOPEDIA_OF_LIFE]

NO_SPECIES_BY_PROVIDED_NAME = 'no_species_by_provided_name'
NO_IMAGES_FOR_SPECIES = 'no_images_for_species'
ERROR = 'error'
CONNECTION_ERROR = 'CONNECTION_ERROR'
JSON_ERROR = 'json_error'

def get_possible_errors():
    return [NO_SPECIES_BY_PROVIDED_NAME,
            NO_IMAGES_FOR_SPECIES,
            ERROR,
            CONNECTION_ERROR,
            JSON_ERROR]

SYSTEM_CHOOSES = 'system_chooses'
USER_CHOOSES = 'user_chooses'

def get_choosing_forms():
    return [SYSTEM_CHOOSES,
            USER_CHOOSES]