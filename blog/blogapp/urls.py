from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('about/', views.acerca_de, name='acerca_de'),
    path('login/', views.login, name='login'), 
    path('signup/', views.signup, name='signup'),  # Página de Acerca de
    path('contact/', views.contacto, name='contacto'),  # Página de Contacto
    path('admin2/', views.nuevo_post, name='admin'),
    path('post_detail/<int:pk>/', views.post_detail, name='post_detail'),
]
