from cStringIO import StringIO
from Bio import Phylo

class NewickTree(object):
    """ Class to wrap phylogeny functions for trees in Newick format.
    """

    def __init__(self, treeString) :
        """
        Init the object using the tree provided as data source. Will parse the tree and throw a NewickError if a
        malformed tree is found.
        :param treeString: String with the tree in Newick format.
        """
        self.treeString = treeString
        self.tree = self._parse(treeString)

    def _parse(self, treeString):
        """
        Parse the tree from the string and return a Tree object.
        :param treeString: String with the tree in Newick format.
        :return: Bio.Phylo.Newick.Tree object with the resulting tree.
        """
        handle = StringIO(treeString)
        return Phylo.read(handle, "newick")

    def getSpeciesNames(self):
        """
        Generates a list of specis names from the tree.
        :return: List of strings with the species names.
        """
        speciesNames = [species.name for species in self.tree.get_terminals()]
        return speciesNames
