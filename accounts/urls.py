from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'rooms', ChatRoomViewSet, basename='room')
router.register(r'messages', MessageViewSet, basename='message')

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
    
     path('api/', include(router.urls)),
]