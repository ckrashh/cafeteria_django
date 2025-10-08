from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # aquí se define 'home'
    path('panel_admin/', views.AdminView.as_view(), name='panel_admin'),
    path('menu/', views.menu, name='menu'),
    path('baristas/', views.baristas, name='baristas'),
    path('resenas/', views.resenas, name='resenas'),
    path('proveedores/', views.proveedores, name='proveedores'),
    path('cafes/', views.cafes, name='cafes'),
    path('resena/nueva/', views.form_resena, name='form_resena'),  # Nueva ruta para el formulario de reseña
    path('admin_usuarios/', views.AdminUsuariosView.as_view(), name='admin_usuarios'),
] 