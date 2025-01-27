from django.urls import path
from .views import (
    FilterByColorView, RegisterOwnerCarView, CarsByOwnerAgeView,
    HeavyCarsRestrictedView, CarOwnerTollView, LightCarsNearTollView, ViolationsView
)

urlpatterns = [
    path('cars/colors/', FilterByColorView.as_view(), name='filter-by-color'),
    path('register/', RegisterOwnerCarView.as_view(), name='register-owner-car'),
    path('cars/owners/age/', CarsByOwnerAgeView.as_view(), name='cars-by-owner-age'),
    path('heavy-cars/restricted/', HeavyCarsRestrictedView.as_view(), name='heavy-cars-restricted'),
    path('toll/<int:car_id>/', CarOwnerTollView.as_view(), name='car-owner-toll'),
    path('light-cars/near-toll/', LightCarsNearTollView.as_view(), name='light-cars-near-toll'),
    path('violations/', ViolationsView.as_view(), name='violations'),
]
