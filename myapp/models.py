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
	organizer = models.ForeignKey(User, on_delete=models.CASCADE)
	seats_available = models.PositiveIntegerField(default=1)

	def __str__(self):
		return self.title


class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)
    seats_booked = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "%s - %s" % (self.event, self.attendee)

