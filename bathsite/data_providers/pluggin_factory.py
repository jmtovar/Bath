from data_providers import phylopic
from data_providers import encyclopedia_of_life
from utils import constants


def get_data_pluggin(pluggin):
    if pluggin == constants.PHYLOPIC:
        return phylopic.PhylopicPluggin()
    elif pluggin == constants.ENCYCLOPEDIA_OF_LIFE:
        return encyclopedia_of_life.EncyclopediaOfLifePluggin()
    else:
        raise Exception('Pluggin reqquest not supported');
	
