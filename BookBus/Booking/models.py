from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    aadhar = models.IntegerField(null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    starting = models.CharField(max_length=255)
    ending = models.CharField(max_length=255)

    def __str__(self):
        return f"Route from {self.starting} to {self.ending}"


class BusStop(models.Model):
    stop_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')

    def __str__(self):
        return self.name


class Bus(models.Model):
    bus_id = models.AutoField(primary_key=True)
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='buses')
    bus_number = models.CharField(max_length=255)
    conductor_name = models.CharField(max_length=255)
    conductor_number = models.CharField(max_length=15)
    
    def __str__(self):
        return f"Id: {self.bus_id} Number: {self.bus_number}"

class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)

    def __str__(self):
        return f"Seat {self.seat_number} on {self.bus.bus_number}"

class Fare(models.Model):
    source = models.ForeignKey(BusStop, related_name='fare_source', on_delete=models.CASCADE)
    destination = models.ForeignKey(BusStop, related_name='fare_destination', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    def __str__(self):
        return f"Rs. {self.price}"


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_user')
    source = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name='bookings_source')
    destination = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name='bookings_destination')
    price = models.ForeignKey(Fare, on_delete=models.CASCADE, related_name='bookings_price')
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='bookings_bus')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user}"
    
    def is_seat_available(self):
        # Check if the seat is available for the given route segment
        conflicting_bookings = Booking.objects.filter(
            bus=self.bus,
            seat=self.seat
        ).exclude(
            destination__arrival_time__lte=self.source.arrival_time
        ).exclude(
            source__arrival_time__gte=self.destination.arrival_time
        )
        return not conflicting_bookings.exists()


class BusSchedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    stop = models.ForeignKey(BusStop, on_delete=models.CASCADE)
    arrival_time = models.TimeField()

    class Meta:
        unique_together = ('bus', 'stop', 'arrival_time')

    def __str__(self):
        return f"Bus {self.bus.bus_number} at stop {self.stop.name} arrives at {self.arrival_time}"
