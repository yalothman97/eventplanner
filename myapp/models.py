from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver


class Event(models.Model):
	title = models.CharField(max_length=120)
	description = models.CharField(max_length=120)
	location = models.CharField(max_length=120)
	date = models.DateField( )
	time = models.TimeField( )
	seats = models.PositiveIntegerField()
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




class Connection(models.Model):
	following =models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
	follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')




class Profile(models.Model):
	person = models.ForeignKey(User, on_delete=models.CASCADE,)
	bio=models.CharField(max_length=280)
	img=models.ImageField(blank=True)
	@receiver(post_save, sender=User)
	def update_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(person=instance).save()
			
