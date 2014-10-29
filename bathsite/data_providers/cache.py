__author__ = 'Jofiel'
from treegenerator.models import CachedURL

class CacheController(object) :

    def tryCache(self, speciesList, database):
        found = dict()
        notFound = []
        for species in speciesList :
            cachedList = CachedURL.objects.filter(species=species, database=database)
            if len(cachedList > 0) :
                print(cachedList)
                found[species] = cachedList[0].url
            else :
                notFound.append(species)
        return found, notFound

    def storeCache(self, speciesDict, database):
        for species in speciesDict.keys() :
            url = speciesDict[species]
            cachedUrl = CachedURL(species = species,database = database, url = url)
            cachedUrl.save()
