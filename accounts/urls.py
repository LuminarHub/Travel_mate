from django.urls import path
from .views import *

urlpatterns = [
    path('login/',LoginView.as_view()),
    path('registration/',RegistrationStudentView.as_view()),
    path('profile/',ProfileView.as_view()),
    path('profile-update/',ProfileUpdateView.as_view()),
    path('trip-create/',TripCreateView.as_view()),
    path('trip-update/<int:pk>/',TripUpdateView.as_view()),
    path('trip-delete/<int:pk>/',TripDeleteView.as_view()),
    path('my-trips/',TripGetView.as_view()),
    path('trip-all/',AllTripsView.as_view()),
]