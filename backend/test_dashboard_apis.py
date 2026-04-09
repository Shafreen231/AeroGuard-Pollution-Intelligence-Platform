#!/usr/bin/env python
import requests

def test_individual_endpoints():
    endpoints = [
        ("Latest readings", "http://localhost:8000/api/monitoring/readings/latest/"),
        ("Pollution zones", "http://localhost:8000/api/monitoring/zones/"),
        ("Vehicles", "http://localhost:8000/api/vehicles/vehicles/"),
        ("Latest predictions", "http://localhost:8000/api/ml/predictions/latest/"),
    ]
    
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            print(f"{name}: Status {response.status_code}")
            if response.status_code != 200:
                print(f"  Error: {response.text[:200]}")
        except Exception as e:
            print(f"{name}: ERROR - {str(e)}")

if __name__ == "__main__":
    test_individual_endpoints()
