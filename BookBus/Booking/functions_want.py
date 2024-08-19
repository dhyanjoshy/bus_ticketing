import pandas as pd
from .models import BusStop, Fare, Route, BusSchedule,Bus
from django.conf import settings
import os


def update_bus_stops():
    file_name = r'price/KA51AR6139A.xlsx'
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    df = pd.read_excel(file_path)

    # Create a dictionary to store route IDs based on stops
    stop_route_mapping = {}

    # Iterate over rows to build stop-route mapping
    for _, row in df.iterrows():
        source_stop = row['Source']
        destination_stop = row['Destination']
        route_id = row['route']  # Ensure this matches your Excel column name

        if source_stop not in stop_route_mapping:
            stop_route_mapping[source_stop] = route_id
        
        if destination_stop not in stop_route_mapping:
            stop_route_mapping[destination_stop] = route_id
    print(stop_route_mapping)


    # Create BusStop objects with route_id
    for stop_name, route_id in stop_route_mapping.items():
        if not BusStop.objects.filter(name=stop_name).exists():
            route_exists = Route.objects.filter(route_id=route_id).exists()
            
            if route_exists:
                route = Route.objects.get(route_id=route_id)
                print(route.ending)
                BusStop.objects.create(
                    name=stop_name,
                    location="Feature Unavailable",
                    route_id=route
                )
            else:
                print(f"Route with ID {route_id} does not exist. Cannot create BusStop {stop_name}.")
        else:
            print(f"BusStop with name {stop_name} already exists.")
        print("Stops_Created")

    # Create Fare objects
    for _, row in df.iterrows():
        source_stop_name = row['Source']
        destination_stop_name = row['Destination'] 
        route_id = row['route'] 

        source_stop_exists = BusStop.objects.filter(name=source_stop_name).exists()
        destination_stop_exists = BusStop.objects.filter(name=destination_stop_name).exists()
        
        route_exists = Route.objects.filter(route_id=route_id).exists()

        if source_stop_exists and destination_stop_exists and route_exists:
            source_stop = BusStop.objects.get(name=source_stop_name)
            destination_stop = BusStop.objects.get(name=destination_stop_name)
            route = Route.objects.get(route_id=route_id)

            Fare.objects.create(
                source=source_stop,
                destination=destination_stop,
                price=row['Price'],
                route=route
            )
        else:
            if not source_stop_exists:
                print(f"BusStop with name {source_stop_name} does not exist.")
            if not destination_stop_exists:
                print(f"BusStop with name {destination_stop_name} does not exist.")
            if not route_exists:
                print(f"Route with ID {route_id} does not exist.")
    return None






def update_shed():
    file_name = r'price/KA51AR6141A_time.xlsx'
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    df = pd.read_excel(file_path)

    # Process each row in the dataframe
    for index, row in df.iterrows():
        stop_name = row['stops']
        time_str = row['time']
        am_pm = row['am/pm']
        bus_number = row['bus']

        time_str = f"{time_str} {am_pm}"
        print(time_str)
        time_obj = pd.to_datetime(time_str, format='%I:%M:%S %p').time()

        # Get the Bus object
        bus = Bus.objects.filter(bus_number=bus_number).first()

        if not bus:
            continue  

        # Get the BusStop object
        stop = BusStop.objects.filter(name=stop_name).first()

        if not stop:
            continue  

        BusSchedule.objects.update_or_create(
            bus=bus,
            stop=stop,
            arrival_time=time_obj,
            defaults={'arrival_time': time_obj}
        )
    return None

