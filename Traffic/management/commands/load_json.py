import json
from django.core.management.base import BaseCommand
from Traffic.models import Owner, Car, Road, TollStation, CarMovement
from django.contrib.gis.geos import Point, MultiLineString

# /home/amirtheengineer/Downloads/testProject-main

class Command(BaseCommand):
    help = "Load data from JSON files into the database"

    def add_arguments(self, parser):
        parser.add_argument('--owners', type=str, help="Path to the owners JSON file")
        parser.add_argument('--roads', type=str, help="Path to the roads JSON file")
        parser.add_argument('--tolls', type=str, help="Path to the toll stations JSON file")
        parser.add_argument('--movements', type=str, help="Path to the car movements JSON file")

    def handle(self, *args, **options):
        # Load Owners
        if options['owners']:
            with open(options['owners'], 'r', encoding='utf-8') as file:
                data = json.load(file)
                for owner_data in data:
                    owner, created = Owner.objects.get_or_create(
                        name=owner_data['name'],
                        national_code=owner_data['national_code'],
                        age=owner_data['age'],
                        total_toll_paid=owner_data['total_toll_paid']
                    )
                    for car_data in owner_data['ownerCar']:
                        Car.objects.get_or_create(
                            id=car_data['id'],
                            owner=owner,
                            car_type=car_data['type'],
                            color=car_data['color'],
                            length=car_data['length'],
                            load_volume=car_data.get('load_valume')
                        )
            self.stdout.write(self.style.SUCCESS("Owners and cars loaded successfully"))

        # Load Roads
        if options['roads']:
            with open(options['roads'], 'r', encoding='utf-8') as file:
                data = json.load(file)
                for road_data in data:
                    name = road_data.get('name')
                    width = road_data.get('width')
                    geom = road_data.get('geom')

                    if not name:
                        self.stdout.write(self.style.ERROR(f"Skipping road with missing name: {road_data}"))
                        continue

                    if not geom:
                        self.stdout.write(self.style.ERROR(f"Skipping road with missing geometry: {road_data}"))
                        continue

                    geom_obj = MultiLineString.from_ewkt(geom)

                    Road.objects.get_or_create(
                        name=name,
                        width=width,
                        geom=geom_obj
                    )
            self.stdout.write(self.style.SUCCESS("Roads loaded successfully"))

        # Load Toll Stations
        if options['tolls']:
            with open(options['tolls'], 'r', encoding='utf-8') as file:
                data = json.load(file)
                for toll_data in data:
                    location = Point.from_ewkt(toll_data['location'])
                    TollStation.objects.get_or_create(
                        name=toll_data['name'],
                        toll_per_cross=toll_data['toll_per_cross'],
                        location=location
                    )
            self.stdout.write(self.style.SUCCESS("Toll stations loaded successfully"))

        # Load Car Movements
        if options['movements']:
            with open(options['movements'], 'r', encoding='utf-8') as file:
                data = json.load(file)
                for movement_data in data:
                    car = Car.objects.get(id=movement_data['car'])
                    location = Point.from_ewkt(movement_data['location'])
                    CarMovement.objects.create(
                        car=car,
                        location=location,
                        date=movement_data['date']
                    )
            self.stdout.write(self.style.SUCCESS("Car movements loaded successfully"))
