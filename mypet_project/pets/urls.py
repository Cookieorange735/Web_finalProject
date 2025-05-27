from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('adopt/', views.adopt_pet, name='adopt_pet'),
    path('pet/', views.view_pet, name='view_pet'),
    path('feed/', views.feed_pet, name='feed_pet'),
    path('clean/', views.clean_pet, name='clean_pet'),
    path('play/', views.play_with_pet, name='play_with_pet'),
]
