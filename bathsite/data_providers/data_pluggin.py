import abc

class DataPluggin(object):
	__metaclass__=abc.ABCMeta
	
	@abc.abstractmethod
	def get_first_image(self, species):
		#returns the url of the first image of the species found in the source
		return
	
	@abc.abstractmethod
	def get_all_images(self, species):
		#returns a list of all the urls for the species found in the source
		return
		