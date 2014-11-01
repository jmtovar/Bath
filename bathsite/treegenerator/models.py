from django.db import models
from datetime import datetime
from django.utils import timezone


class Request(models.Model):
	date = models.DateTimeField('date requested')
	status = models.CharField(max_length=10)

	#Prevents requests from saving without the date
	def save(self, *args, **kwargs):
		if self.date is None:
			self.date = timezone.now()
		super(self.__class__, self).save(*args, **kwargs)
		
class Species(models.Model):
	name = models.CharField(max_length=200)

class Request_Species(models.Model):
	request = models.ForeignKey(Request)
	species = models.ForeignKey(Species)

class CachedURL(models.Model):
    species = models.CharField(max_length = 300)
    database = models.CharField(max_length = 100)
    url = models.CharField(max_length = 500)
    date = models.DateTimeField(default=timezone.now)
