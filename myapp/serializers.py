from rest_framework import serializers
from myapp.models import Event, Attendance, Profile, Connection
from django.contrib.auth.models import User
# from rest_framework_jwt.settings import api_settings


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        return validated_data

class EventListSerializer(serializers.ModelSerializer):
	class Meta:
	    model = Event
	    fields = '__all__'

class CreateEventSerializer(serializers.ModelSerializer):
	class Meta:
	    model = Event
	    exclude=['organizer']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['seats_booked']


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        exclude = ['following','follower']