__author__ = 'Jofiel'
from treegenerator.models import CachedURL
from django.utils import timezone

class CacheController(object) :

    def tryCache(self, speciesList, database, minutes = 1):
        found = dict()
        notFound = []
        for species in speciesList :
            print("Trying cache for {}".format(species))

            cachedList = CachedURL.objects.filter(species=species, database=database).filter(date__range = [timezone.now()-timezone.timedelta(minutes = minutes),timezone.now()])
            if len(cachedList) > 0 :
                print("Found cache for {}".format(species))
                found[species] = cachedList[0].url
            else :
                notFound.append(species)
        return found, notFound

    def storeCache(self, speciesDict, database):
        for species in speciesDict.keys() :
            print("Storing {} {}".format(species, speciesDict[species]))
            url = speciesDict[species]
            cachedUrl = CachedURL(species = species,database = database, url = url)
            cachedUrl.save()
