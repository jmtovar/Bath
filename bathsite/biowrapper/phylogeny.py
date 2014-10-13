from cStringIO import StringIO
from Bio import Phylo

class NewickTree(object):

    def __init__(self, treeString) :
        self.treeString = treeString
        self.tree = self._parse(treeString)

    def _parse(self, treeString):
        handle = StringIO(treeString)
        return Phylo.read(handle, "newick")

    def getSpeciesNames(self):
        speciesNames = [species.name for species in self.tree.get_terminals()]
        return speciesNames
