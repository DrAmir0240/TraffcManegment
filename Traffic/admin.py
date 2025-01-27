from django.contrib import admin
from .models import Owner, Car, Road, TollStation, CarMovement

# Register your models here.

admin.site.register(Owner)
admin.site.register(Car)
admin.site.register(Road)
admin.site.register(TollStation)
admin.site.register(CarMovement)
