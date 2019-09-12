from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from myapp.forms import UserSignup, UserLogin,ProfileForm
from django.contrib import messages
from .models import Event, Attendance,Profile,Connection
from .forms import EventForm, BookTicket
import datetime
from django.db.models import Q
from rest_framework.generics import(ListAPIView, CreateAPIView,
RetrieveUpdateAPIView, DestroyAPIView)
from .serializers import (EventListSerializer, UserCreateSerializer,
EventAttendanceSerializer,CreateEventSerializer,BookingSerializer, FollowingSerializer)
from django.contrib.auth.models import User
from django.core.mail import send_mail


def home(request):
    return render(request, 'home.html')


class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                if auth_user.is_authenticated:
                    return redirect('dashboard')
                else:
                    return redirect('events')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")


def cancel(request,event_id):
    


    attend=Attendance.objects.get(attendee_id=request.user.id,event_id=event_id)
    if not attend.booked_on.day >= datetime.date.today().day + 3:
        messages.warning(request, "You cannot Cancel the Booking")
    else:
        attend.delete()
        messages.success(request, "You have successfully Cancelled the event")
    return redirect("dashboard")


def dashboard(request):
    events = Event.objects.filter(organizer = request.user)
    
    
    context = {
        'events': events,
 
    }
    return render(request, 'dashboard.html', context)


def create_event(request):
    form = EventForm()
    if not request.user.is_authenticated:
        messages.warning(request, "Access Denied. You need to be an event organizer.")
        return redirect('home')
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event=form.save(commit=False)
            event.organizer=request.user
            event.save()
            emails=[]
            x=0
            for follower in request.user.followers.all().values_list('follower',flat=True):
                print(follower)
                email=User.objects.get(id=follower).email
                emails.append(email)
            send_mail(
                'New Event by '+str(event.organizer.username)+'!',
               " Don't miss out on "+event.title +'!',
                'codeddjangoproject@gmail.com',
                emails,
                fail_silently=False
                )
            messages.success(request, "Event Created Successfully")
            return redirect("dashboard")
    context = {
        'form': form
    }
    return render(request, 'create.html', context)


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    attendance = Attendance.objects.filter(event = event)
    context = {
        "event": event,
        'attendance': attendance,
    }
    return render(request, 'detail.html', context)


def profile(request, user_id):
    user=User.objects.get(id=user_id)
    profile = Profile.objects.get(person=user)
    events = Event.objects.filter(organizer=user)
    followers_of_user = False
    if request.user in Connection.objects.filter(following=user):
        followers_of_user=True


    if request.POST.get('follow'):
        obj, created = Connection.objects.get_or_create(following=user, follower=request.user)
        followers_of_user=True

    elif request.POST.get('Unfollow'):
        try:
            Connection.objects.get(following=user, follower=request.user).delete()
            followers_of_user = False

        except:
            pass
    context = {
       "profile": profile,
       "events": events,
       "followers_of_user": followers_of_user
    }
    return render(request, 'profile.html', context)


def update_profile(request, user_id):
    user=User.objects.get(id=user_id)
    profile = Profile.objects.get(person=user)
    form = ProfileForm(instance=profile)
    form2=UserSignup(instance=request.user)
    if request.method == "POST":
         form = ProfileForm(request.POST,request.FILES , instance=profile)
         form2 = UserSignup(request.POST, instance=request.user)
         if form.is_valid():
            form.save()
         if form2.is_valid():
            user = form2.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(request, user)
            



            messages.success(request, "Profile Updated Successfully")
            return redirect("profile", user_id)
    context = {
        "profile": profile,
        'form':form,
        'form2':form2,

    }
    return render(request, 'updateProfile.html', context)


def get_followers(request,user_id):
    user=User.objects.get(id=user_id)
    followers=Connection.objects.filter(following= user)
    context={
        'followers':followers,
    }
    return render(request, 'followers.html', context)


def get_following(request,user_id):
    user=User.objects.get(id=user_id)
    following=Connection.objects.filter(follower = user)
    
    context={
        'followings':following,
    }
    return render(request, 'following.html', context)
def update_event(request, event_id):
    event = Event.objects.get(id=event_id)
    form = EventForm(instance=event)
    if not request.user == event.organizer:
        messages.warning(request, "Access Denied. You need to be the event organizer.")
        return redirect('home')
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect("event-detail", event_id)
    context = {
        'form': form,
        'event':event,
    }
    return render(request, 'update.html', context)


def book_event(request,event_id):
    event = Event.objects.get(id=event_id)
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login to Book")
        return redirect('login')
    form = BookTicket()
    if request.method == "POST":
        form = BookTicket(request.POST)
        if form.is_valid():
            booking=form.save(commit=False)
            booking.event=event
            booking.attendee=request.user
            seats_available=event.seats_available()
            if seats_available==0 :
                messages.warning(request, "FULLY BOOKED!")
                return redirect("event-detail", event_id)
            elif seats_available>=booking.seats_booked:
                if booking.seats_booked==0:
                    messages.warning(request, "Please specify a number!")
                    return redirect("book-event", event_id)
                
                attendant= Attendance.objects.filter(attendee=request.user,event=event).first()
                if attendant :
                    attendant.seats_booked += booking.seats_booked
                    attendant.save()
                    send_mail(
                        'Booking Confirmation',
                        'confirmation for '+ event.title +" on  "+str(event.date)+" at " +str(event.time),
                        'codeddjangoproject@gmail.com',
                        [request.user.email],
                        fail_silently=False,
                    )
                    messages.success(request, "Seats Booked!")
                else:
                    booking.save()
                    send_mail(
                        'Booking Confirmation',
                        'confirmation for '+ event.title +" on the "+str(event.date)+" at " +str(event.time),
                        'codeddjangoproject@gmail.com',
                        [request.user.email],
                        fail_silently=False,
                    )
                    messages.success(request, "Seats Booked!")
                return redirect("event-detail", event_id)
            else:
                messages.warning(request, "Requested seats not available")
            
    context={
    'event':event,
    'form':form
    }                     
    return render(request,'book.html',context)


def events_list(request):
    events = Event.objects.filter(date__gte=datetime.date.today())
    query = request.GET.get("q")
    if query:
        events = events.filter(Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(organizer__username__icontains=query)
            ).distinct()
    context = {
        'events': events
    }
    return render(request, 'events.html', context)


class EventListView(ListAPIView):
    queryset = Event.objects.filter(date__gte=datetime.date.today())
    serializer_class = EventListSerializer


class OrganizerListView(ListAPIView):
    serializer_class = EventListSerializer


    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(organizer_id=self.kwargs['user_id'])


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer


class MyEventsListView(ListAPIView):
    serializer_class = EventListSerializer
    def get_queryset(self):
        user = self.request.user
        return Attendance.objects.filter(attendee=user)



class MyBookedEventsView(ListAPIView):
    serializer_class = EventAttendanceSerializer
    def get_queryset(self):
        user = self.request.user
        return Attendance.objects.filter(attendee=self.request.user)

class GetAttendance(ListAPIView):
    serializer_class = EventAttendanceSerializer


    def get_queryset(self):
        event = Event.objects.get(id=self.kwargs['event_id'])
        return event.attendees.all()


class CreateEvent(CreateAPIView):
    serializer_class = CreateEventSerializer


    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class UpdateEvent(RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = CreateEventSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'


class BookEvent(CreateAPIView):
    serializer_class = BookingSerializer


    def perform_create(self, serializer):
        serializer.save(event_id=self.kwargs['event_id'],attendee=self.request.user)


class FollowProfile(CreateAPIView):
    serializer_class = FollowingSerializer


    def perform_create(self, serializer):
        serializer.save(following_id=self.kwargs['user_id'],follower=self.request.user)


class UnFollowProfile(DestroyAPIView):
    serializer_class = FollowingSerializer
    lookup_field = 'following_user_id'
    lookup_url_kwarg = 'user_id'


    def get_queryset(self):
        queryset = Connection.objects.get(follower=self.request.user,following=self.kwargs['user_id'])
        queryset.delete()
        return queryset