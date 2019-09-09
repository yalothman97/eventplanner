from django.contrib import admin
from django.urls import path, include

from myapp import views

from rest_framework_simplejwt.views import TokenObtainPairView


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
	path('lists/', views.EventListView.as_view()),
	# path('token/', TokenObtainPairView.as_view(), name='token'),
	path('myevents/', views.OrganizerListView.as_view()),
	path('apiregister/', views.UserCreateAPIView.as_view()),
	path('apilogin/', views.UserLoginAPIView.as_view()),




]
