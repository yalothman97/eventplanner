from django.db import models
from django.contrib.auth.models import User
import datetime


class Event(models.Model):
	title = models.CharField(max_length=120)
	description = models.CharField(max_length=120)
	location = models.CharField(max_length=120)
	date = models.DateField(blank=True, auto_now=False)
	time = models.TimeField(blank=True, auto_now=False)
	seats = models.PositiveIntegerField(default=1)
	organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
	# seats_available = models.PositiveIntegerField(default=1)

	def __str__(self):
		return self.title


	def booked_seats(self):
		return sum(self.attendees.all().values_list('seats_booked',flat=True))
		

	def seats_available(self):
		return self.seats-self.booked_seats()




class Attendance(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
	
	attendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attended')
	seats_booked = models.PositiveIntegerField(default=1)

	def __str__(self):
		return "%s - %s" % (self.event, self.attendee)

