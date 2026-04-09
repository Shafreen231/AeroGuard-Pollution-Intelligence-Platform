#!/usr/bin/env python
import requests
import json

def test_api_response():
    print("Testing API response structure...")
    
    try:
        # Test sensor readings
        response = requests.get("http://localhost:8000/api/monitoring/readings/latest/", timeout=10)
        print(f"\n=== Sensor Readings ===")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Count: {len(data)}")
            if len(data) > 0:
                print(f"Sample structure: {list(data[0].keys())}")
                print(f"Sample data: lat={data[0].get('latitude')}, lng={data[0].get('longitude')}, aqi={data[0].get('aqi')}")
        
        # Test pollution zones
        response = requests.get("http://localhost:8000/api/monitoring/zones/", timeout=10)
        print(f"\n=== Pollution Zones ===")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                zones = data['results']
                print(f"Count: {len(zones)}")
                if len(zones) > 0:
                    print(f"Sample structure: {list(zones[0].keys())}")
                    print(f"Sample zone: {zones[0]}")
        
        # Test vehicles
        response = requests.get("http://localhost:8000/api/vehicles/vehicles/", timeout=10)
        print(f"\n=== Vehicles ===")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                vehicles = data['results']
                print(f"Count: {len(vehicles)}")
                if len(vehicles) > 0:
                    print(f"Sample structure: {list(vehicles[0].keys())}")
                    vehicle = vehicles[0]
                    print(f"Sample vehicle: {vehicle.get('name')} at {vehicle.get('current_latitude')}, {vehicle.get('current_longitude')}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api_response()
