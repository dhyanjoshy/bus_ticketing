from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .functions_want import update_bus_stops,update_shed
from django.contrib.auth.decorators import user_passes_test
from .checks import admin_check,login_required
from .models import Bus, BusStop, BusSchedule,Fare, Booking, Seat,Route
from  datetime import datetime
from .forms import UserRegisterForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from .routes import route




def index(request):
    bus_stops = BusStop.objects.all()  # Fetch all BusStop objects
    return render(request, 'index2.html', {'bus_stops': bus_stops})

def indextry(request):
    bus_stops = BusStop.objects.all()  # Fetch all BusStop objects
    return render(request, 'seat_details.html', {'bus_stops': bus_stops})


def signup_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'signup_og.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login_og.html')

def logout_view(request):
    logout(request)
    return redirect('/')

# @login_required
def buslist(request):
    if request.method == "POST":
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        time = request.POST.get('time')
        print(f"Time : {time}")
        
        # Convert the time to a datetime.time object
        try:
            time_obj = datetime.strptime(time, '%H:%M').time()
        except ValueError:
            return HttpResponse("Invalid time format. Please enter time in HH:MM format.")
        
        # Fetch the source and destination BusStop objects
        try:
            source_stop = BusStop.objects.get(name=source)
            destination_stop = BusStop.objects.get(name=destination)
        except BusStop.DoesNotExist:
            return HttpResponse("Invalid source or destination stop selected.")

        # Filter buses based on the conditions
        buses = Bus.objects.filter(
            route_id=source_stop.route_id, 
            busschedule__stop=source_stop, 
            busschedule__arrival_time__gt=time_obj
        ).distinct()

        # Create a dictionary to store arrival times for each bus at the source stop
        context = {}
        for bus in buses:
            context[bus.bus_number] = {}
            context[bus.bus_number]['bus_number'] = bus.bus_number
            context[bus.bus_number]['source'] = source
            context[bus.bus_number]['destination'] = destination
            context[bus.bus_number]['source_time'] = BusSchedule.objects.filter(bus=bus, stop=source_stop).first().arrival_time.strftime("%I:%M %p")
            context[bus.bus_number]['destination_time']  = BusSchedule.objects.filter(bus=bus, stop=destination_stop).first().arrival_time.strftime("%I:%M %p")
            context[bus.bus_number]['conduct_name'] = bus.conductor_name
            context[bus.bus_number]['conduct_num'] = bus.conductor_number
            context[bus.bus_number]['price'] = Fare.objects.filter(source=source_stop, destination=destination_stop).first()
        
        print(context)
        return render(request, 'bus_list.html', {'buses':context})

    return HttpResponse("Invalid Request")

@login_required
def bus_detail(request, bus_number, source, destination):
    bus = get_object_or_404(Bus, bus_number=bus_number)
    source = get_object_or_404(BusStop, name=source)
    destination = get_object_or_404(BusStop, name=destination)


    stop_order = route[bus.route_id.route_id]
    print(stop_order)
    
    source_index = stop_order.index(source.name)
    destination_index = stop_order.index(destination.name)

    if source_index > destination_index:
        raise ValueError("Source must come before destination in the route")

    
    segment_start = source_index
    segment_end = destination_index
    
    
    bookings_in_bus = Booking.objects.filter(
        bus=bus,
        date__isnull=False,
    )

    overlapping_bookings = []

    for booking in bookings_in_bus:
        booking_start_index = stop_order.index(booking.source.name)
        booking_end_index = stop_order.index(booking.destination.name)
        booking_stops = set(range(booking_start_index,booking_end_index))
        print(f"booking stops = {booking_stops}")
        checking_stops = set(range(segment_start,segment_end))
        print(f"checking stops = {checking_stops}")
        inter = booking_stops.intersection(checking_stops)
        print(f"intersection = {inter}")
        if inter != set():
            overlapping_bookings.append(booking)
        else:
            pass
    
    print(overlapping_bookings)
    
    all_seats = Seat.objects.filter(bus=bus)
    available_seats = all_seats

    for booking in overlapping_bookings:
        available_seats = available_seats.exclude(seat_number=booking.seat.seat_number)
    print(f"available_seats = {available_seats}")

    context = {
        'bus': bus,
        'source': source,
        'destination': destination,
        'available_seats': available_seats,
    }
    print(context)
    return render(request, 'seat_details.html', context)


@login_required
def create_booking_view(request):
    if request.method == 'POST':
        user = request.user
        bus_id = request.POST.get('bus_id')
        seat_no = request.POST.get('seat_no')
        source = request.POST.get('source')
        destination = request.POST.get('destination')

        print(user)
        print(bus_id)
        print(seat_no)
        print(source)
        print(destination)

        bus = get_object_or_404(Bus, pk=bus_id)
        source = get_object_or_404(BusStop, name=source)
        destination = get_object_or_404(BusStop, name=destination)
        price = Fare.objects.filter(source=source, destination=destination).first()
        seat = get_object_or_404(Seat, bus = bus, seat_number = seat_no)
        print(seat)

        # Create the Booking object
        booking = Booking.objects.create(
            user=user,
            bus_id=bus.bus_id,
            seat=seat,
            source=source,
            destination=destination,
            price=price
        )

        return redirect('booking_confirmation', booking_id=booking.booking_id)

    return redirect('bus_list')



@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'booking_conf.html', {'booking': booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings_final.html', {'bookings': bookings})



@user_passes_test(admin_check)
def update_bus_stops_and_fares(request):
    update_bus_stops()
    return HttpResponse("updated_successfully")

@user_passes_test(admin_check)
def update_schedule(request):
    update_shed()
    return HttpResponse("updated_successfully")