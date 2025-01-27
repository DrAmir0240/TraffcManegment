from rest_framework import serializers
from .models import Owner, Car, Road, TollStation, CarMovement

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class OwnerSerializer(serializers.ModelSerializer):
    ownerCar = CarSerializer(many=True)
    class Meta:
        model = Owner
        fields = '__all__'

class RoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Road
        fields = '__all__'

class TollStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TollStation
        fields = '__all__'

class CarMovementSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = CarMovement
        fields = '__all__'
