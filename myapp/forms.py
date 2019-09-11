from django import forms
from django.contrib.auth.models import User
from .models import Event,Attendance,Profile

class UserSignup(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email' ,'password']

		widgets={
		'password': forms.PasswordInput(),
		}


class UserLogin(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())


class EventForm(forms.ModelForm):
	# date=forms
	class Meta:
		model = Event
		# fields = ['title', 'description', 'location', 'seats', 'date', 'time', ]
		exclude=['organizer']
		widgets = {
			'date': forms.DateInput(attrs={'type':'date'}),
			'time': forms.TimeInput(attrs={'type':'time'})
		}

class BookTicket(forms.ModelForm):
	class Meta:
		model = Attendance
		fields = ['seats_booked']

class ProfileForm(forms.ModelForm):
	class Meta:
		model=Profile
		labels = {
			'bio': 'Bio:',
			'img': 'Upload Image:'
		}
		exclude=['person']

