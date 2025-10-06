from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),  # aquí se define 'home'
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]