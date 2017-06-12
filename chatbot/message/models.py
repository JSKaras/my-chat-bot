from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Room(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)

#	def __unicode__(self): # for python2
#		return self.name

	def __str__(self): # for python3
		return self.name

class Reservation(models.Model):
	id = models.AutoField(primary_key=True)
	#room_name = models.CharField(max_length=50, default="")
	room = models.ForeignKey(Room)
	request_time = models.DateTimeField('Request Time')
	reserv_time = models.DateTimeField('Reservation Time')
	end_time = models.DateTimeField('End Time')
	reserved_field = models.CharField(max_length=200, default="")

#	def __unicode__(self): # for python2
#		return self.room

	def __str__(self):    # for python3
		return self.room.name

class History(models.Model):
	id = models.AutoField(primary_key=True)
	#room_name = models.CharField(max_length=50)
	room = models.ForeignKey(Room)
	request_time = models.DateTimeField('Request Time')
	reserv_time = models.DateTimeField('Reservation Time')
	end_time = models.DateTimeField('End Time')
	reserved_field = models.CharField(max_length=200, default="")

#	def __unicode__(self):
#		return self.room

	def __str__(self):
		return self.room.name

