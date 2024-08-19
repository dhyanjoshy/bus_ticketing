from django.contrib import admin
from .models import Profile, Booking, Bus, BusStop, Route, BusSchedule, Fare, Seat

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'date_of_birth', 'aadhar')
    search_fields = ('user__username', 'phone_number', 'aadhar')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'source', 'destination', 'price', 'bus', 'seat', 'date')
    list_filter = ('user', 'source', 'destination', 'bus', 'seat', 'date')
    search_fields = ('user__username', 'source__name', 'destination__name', 'bus__bus_number', 'seat__seat_number')

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_id', 'bus_number', 'route_id', 'conductor_name', 'conductor_number')
    list_filter = ('route_id',)
    search_fields = ('bus_number', 'conductor_name')

@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'route_id')
    list_filter = ('route_id',)
    search_fields = ('name', 'location')

    change_list_template = 'admin/booking/busstop/change_list.html'

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('route_id', 'starting', 'ending')
    search_fields = ('starting', 'ending')

@admin.register(BusSchedule)
class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ('bus', 'stop', 'arrival_time')
    list_filter = ('bus', 'stop')
    search_fields = ('bus__bus_number', 'stop__name')

    change_list_template = 'admin/booking/busstop/change_list.html'

@admin.register(Fare)
class FareAdmin(admin.ModelAdmin):
    list_display = ('source', 'destination', 'price', 'route')
    list_filter = ('route',)
    search_fields = ('source__name', 'destination__name')

    change_list_template = 'admin/booking/busstop/change_list.html'

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('bus', 'seat_number')
    list_filter = ('bus',)
    search_fields = ('bus__bus_number', 'seat_number')
