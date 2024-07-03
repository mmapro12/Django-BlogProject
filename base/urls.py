from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),
    path('login/', views.loginPage, name='login-page'),
    path('register/', views.registerPage, name='register-page'),
    path('logout/', views.logoutUser, name='logout-page'),
    path('profile/<str:pk>/', views.profile, name='profile')
]
