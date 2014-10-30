__author__ = 'Jofiel'
from treegenerator.models import CachedURL
from django.utils import timezone

class CacheController(object):
    """ Class to control cache access.
    """

    def tryCache(self, speciesList, database, minutes = 60):
        """
        Tries to find if there is a previous register for the species/database in the cache. All data is kept in the
        database. Probably needs some cleanup
        :param speciesList: List of species names as they are queried against the database (with spaces in names).
        :param database: Name of the database. Just the name as a string.
        :param minutes: Number of minutes for cache expiry. Default 1 hour.
        :return: dictionary with those species found in the cache species=>url, list of species not found in the cache.
        """
        found = dict()
        notFound = []
        for species in speciesList :
            print("Trying cache for {}".format(species))

            cachedList = CachedURL.objects.filter(species=species, database=database)\
                .filter(date__range = [timezone.now()-timezone.timedelta(minutes = minutes),timezone.now()])
            if len(cachedList) > 0 :
                print("Found cache for {}".format(species))
                found[species] = cachedList[0].url
            else :
                notFound.append(species)
        return found, notFound

    def storeCache(self, speciesDict, database):
        """ Store values got from database in cache.
        :param speciesDict: Dictionary with the species->url to save in cache
        :param database: Name of the database where this urls were found.
        """
        for species in speciesDict.keys() :
            print("Storing {} {}".format(species, speciesDict[species]))
            url = speciesDict[species]
            cachedUrl = CachedURL(species = species,database = database, url = url)
            cachedUrl.save()
