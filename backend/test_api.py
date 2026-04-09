#!/usr/bin/env python
import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pollution_monitor.settings')
django.setup()

from monitoring.models import SensorReading, PollutionZone
from vehicles.models import Vehicle
from ml_prediction.models import PollutionPrediction

def test_sample_data():
    print("=== Testing Sample Data Generation ===")
    
    # Check current data
    print(f"Sensor readings: {SensorReading.objects.count()}")
    print(f"Pollution zones: {SensorReading.objects.count()}")
    print(f"Vehicles: {Vehicle.objects.count()}")
    print(f"Predictions: {PollutionPrediction.objects.count()}")
    
    # Check first few readings
    if SensorReading.objects.exists():
        print("\nFirst 3 sensor readings:")
        for reading in SensorReading.objects.all()[:3]:
            print(f"  - Location: {reading.latitude}, {reading.longitude}, AQI: {reading.aqi}")
    
    # Check zones
    if PollutionZone.objects.exists():
        print("\nPollution zones:")
        for zone in PollutionZone.objects.all():
            print(f"  - {zone.name}: {zone.zone_type} at {zone.coordinates}")
    
    # Check vehicles
    if Vehicle.objects.exists():
        print("\nVehicles:")
        for vehicle in Vehicle.objects.all()[:3]:
            print(f"  - {vehicle.name}: {vehicle.status} at {vehicle.current_latitude}, {vehicle.current_longitude}")

if __name__ == "__main__":
    test_sample_data()
