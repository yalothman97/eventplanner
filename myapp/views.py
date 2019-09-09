from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from myapp.forms import UserSignup, UserLogin
from django.contrib import messages
from .models import Event, Attendance
from .forms import EventForm, BookTicket
import datetime
from django.db.models import Q
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import EventListSerializer, UserCreateSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView


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


def dashboard(request):
	events = Event.objects.filter(organizer = request.user)
	context = {
		'events': events
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
            if seats_available<=0 :
                messages.warning(request, "FULLY BOOKED!")
                return redirect("event-detail", event_id)

            elif seats_available>=booking.seats_booked:
                booking.save()
                messages.success(request, "Seats Booked!")
                return redirect("event-detail", event_id)
            else:
                messages.warning(request, "Requested seats not available")
            #     return redirect("book-event", event_id)

            # if booking.seats_booked>event.seats_available:
            #     messages.warning(request, "Requested seats not available")
            #     return redirect("book-event", event_id)

            #     # return redirect('home')

            # else:
            #     event.seats_available -= booking.seats_booked
            #     booking.save()
            #     event.save()

                # messages.success(request, "Seats Booked!")
                # return redirect("event-detail", event_id)
            
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
        return Event.objects.filter(organizer=user)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        my_data = request.data
        serializer = UserLoginSerializer(data=my_data)
        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.data
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


# class myEventsListView(ListAPIView):
#     serializer_class = EventListSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return Event.objects.filter(organizer=user)
