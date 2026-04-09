#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pollution_monitor.settings')
django.setup()

from monitoring.views import SensorReadingViewSet, PollutionZoneViewSet
from vehicles.views import VehicleViewSet
from ml_prediction.views import PollutionPredictionViewSet
from rest_framework.test import APIRequestFactory

def generate_sample_data():
    print("=== Generating Sample Data ===")
    
    # Create a mock request
    factory = APIRequestFactory()
    request = factory.get('/')
    
    # Initialize ViewSets and trigger data generation
    print("Generating sensor readings...")
    sensor_viewset = SensorReadingViewSet()
    sensor_viewset.request = request
    sensor_viewset.get_queryset()
    
    print("Generating pollution zones...")
    zone_viewset = PollutionZoneViewSet()
    zone_viewset.request = request
    zone_viewset.get_queryset()
    
    print("Generating vehicles...")
    vehicle_viewset = VehicleViewSet()
    vehicle_viewset.request = request
    vehicle_viewset.get_queryset()
    
    print("Generating predictions...")
    prediction_viewset = PollutionPredictionViewSet()
    prediction_viewset.request = request
    prediction_viewset.get_queryset()
    
    # Check results
    from monitoring.models import SensorReading, PollutionZone
    from vehicles.models import Vehicle
    from ml_prediction.models import PollutionPrediction
    
    print(f"\nGenerated:")
    print(f"  - Sensor readings: {SensorReading.objects.count()}")
    print(f"  - Pollution zones: {PollutionZone.objects.count()}")
    print(f"  - Vehicles: {Vehicle.objects.count()}")
    print(f"  - Predictions: {PollutionPrediction.objects.count()}")
    
    # Show some sample data
    if SensorReading.objects.exists():
        print(f"\nSample sensor reading:")
        reading = SensorReading.objects.first()
        print(f"  Location: {reading.latitude:.4f}, {reading.longitude:.4f}")
        print(f"  AQI: {reading.aqi}, PM2.5: {reading.pm25:.1f}")
        
    if PollutionZone.objects.exists():
        print(f"\nSample pollution zone:")
        zone = PollutionZone.objects.first()
        print(f"  {zone.name}: {zone.zone_type} at {zone.coordinates}")
        
    if Vehicle.objects.exists():
        print(f"\nSample vehicle:")
        vehicle = Vehicle.objects.first()
        print(f"  {vehicle.name}: {vehicle.status}")
        print(f"  Location: {vehicle.current_latitude:.4f}, {vehicle.current_longitude:.4f}")

if __name__ == "__main__":
    generate_sample_data()
