from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from myapp import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
	path('admin/', admin.site.urls),
	path('', views.home, name='home'),
	path('signup/', views.Signup.as_view(), name='signup'),
	path('login/', views.Login.as_view(), name='login'),
	path('logout/', views.Logout.as_view(), name='logout'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('dashboard/create/', views.create_event, name='create-event'),
	path('dashboard/<int:event_id>/update/', views.update_event, name='update-event'),
	path('events/<int:event_id>/book/', views.book_event, name='book-event'),
	path('events/', views.events_list, name='events'),
	path('events/<int:event_id>/', views.event_detail, name='event-detail'),
	path('profile/<int:user_id>/', views.profile, name='profile'),
	path('profile/<int:user_id>/update', views.update_profile, name='update-profile'),
	path('profile/<int:user_id>/following', views.get_following, name='following'),
	path('profile/<int:user_id>/followers', views.get_followers, name='followers'),






	path('api/login/', TokenObtainPairView.as_view(), name='token'),

	path('api/events/', views.EventListView.as_view()),
	path('api/myevents', views.OrganizerListView.as_view()),
	path('api/register/', views.UserCreateAPIView.as_view()),
	path('api/booked', views.MyEventsListView.as_view()),
	path('api/<int:event_id>/attendance', views.GetAttendance.as_view()),
	path('api/create/', views.CreateEvent.as_view()),
	path('api/<int:event_id>/update', views.UpdateEvent.as_view()),
	





]

urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
