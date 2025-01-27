from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Owner, Car, Road, TollStation, CarMovement
from .serializers import OwnerSerializer, RoadSerializer, TollStationSerializer, CarMovementSerializer, CarSerializer


# Create your views here.
class FilterByColorView(APIView):
    def get(self, request):
        cars = Car.objects.filter(color__in=['red', 'blue'])
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterOwnerCarView(APIView):
    def post(self, request):
        owner_serializer = OwnerSerializer(data=request.data.get('owner'))
        car_serializer = CarSerializer(data=request.data.get('car'))
        if owner_serializer.is_valid() and car_serializer.is_valid():
            owner = owner_serializer.save()
            car = car_serializer.save(owner=owner)
            return Response({
                'owner': owner_serializer.data,
                'car': car_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'owner_errors': owner_serializer.errors,
            'car_errors': car_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CarsByOwnerAgeView(APIView):
    def get(self, request):
        cars = Car.objects.filter(owner__age__gt=70)
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HeavyCarsRestrictedView(APIView):
    def get(self, request, *args, **kwargs):

        narrow_roads = Road.objects.filter(width__lt=20)

        if not narrow_roads.exists():
            return JsonResponse({'error': 'No narrow roads found'}, status=404)

        heavy_cars = Car.objects.filter(car_type='big')

        query = Q()
        for road in narrow_roads:
            query |= Q(location__intersects=road.geom)

        movements = CarMovement.objects.filter(
            car__in=heavy_cars
        ).filter(query)

        data = [
            {
                'car': str(movement.car),
                'location': movement.location.coords,
                'date': movement.date,
            }
            for movement in movements
        ]

        return JsonResponse({'movements': data}, safe=False)


class CarOwnerTollView(APIView):
    def get(self, request, car_id):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        movements = CarMovement.objects.filter(car__id=car_id, date__range=[start_date, end_date])
        total_toll = sum([movement.car.owner.total_toll_paid for movement in movements])
        return Response({'car_id': car_id, 'total_toll': total_toll}, status=status.HTTP_200_OK)


from django.contrib.gis.db.models.functions import Distance

class LightCarsNearTollView(APIView):
    def get(self, request):
        toll_station = TollStation.objects.get(id=1)
        nearby_cars = Car.objects.filter(
            type='small',
            location__distance_lte=(toll_station.location, 600)
        )
        serializer = CarSerializer(nearby_cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ViolationsView(APIView):
    def get(self, request):
        owners = Owner.objects.filter(total_toll_paid__gt=0).order_by('-total_toll_paid')
        data = owners.values('name', 'national_code', 'total_toll_paid')
        return Response(data, status=status.HTTP_200_OK)
