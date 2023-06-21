from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('booking/', views.index, name='index'),
    path('booking/reservations', views.reservations, name='reservations'),
    path('booking/add_reservation', views.add_reservation, name='add_reservation'),
    path('booking/login', views.user_login),
    path('booking/register', views.register, name='register'),
    path('booking/logout', views.logout_user, name='logout'),
    path('booking/delete/<rid>', views.delete, name="delete"),
    path('booking/user_reservations', views.user_reservations, name='user_reservations'),
    path('booking/cancel/<rid>', views.cancel, name='cancel')
]