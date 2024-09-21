from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("indextry", views.indextry, name="indextry"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup_view, name="signup"),
    path("update_price", views.update_bus_stops_and_fares, name="update_price"),
    path("update_schedule", views.update_schedule, name="update_schedule"),
    path("buslist", views.buslist, name="buslist"),
    path('bus_detail/<str:bus_number>/<str:source>/<str:destination>/', views.bus_detail, name='bus_detail'),
    path('create-booking/', views.create_booking_view, name='create_booking'),
    path('booking_confirmation/<int:booking_id>', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]