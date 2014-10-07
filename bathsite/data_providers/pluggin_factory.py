from data_providers import phylopic
from data_providers import encyclopedia_of_life

PHYLOPIC = 'Phylopic'
ENCYCLOPEDIA_OF_LIFE = 'Encyclopedia of life'
DEFAULT = 'phylopic'

def get_data_pluggin(pluggin):
	if pluggin == PHYLOPIC:
		return phylopic.PhylopicPluggin()
	elif pluggin == ENCYCLOPEDIA_OF_LIFE:
		return encyclopedia_of_life.EncyclopediaOfLifePluggin()
	else:
		raise Exception('Pluggin reqquest not supported');
	
