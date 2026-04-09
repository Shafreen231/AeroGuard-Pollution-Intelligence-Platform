#!/usr/bin/env python
import requests
import json

def test_api_endpoints():
    base_url = "http://localhost:8000/api"
    
    endpoints = [
        "/monitoring/readings/",
        "/monitoring/zones/",
        "/vehicles/vehicles/",
        "/ml/predictions/"
    ]
    
    print("=== Testing API Endpoints ===")
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"\n{endpoint}")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and 'results' in data:
                    count = len(data['results'])
                    print(f"Count: {count}")
                    if count > 0:
                        # Show first item structure
                        first_item = data['results'][0]
                        print(f"Sample keys: {list(first_item.keys())[:5]}")
                elif isinstance(data, list):
                    count = len(data)
                    print(f"Count: {count}")
                    if count > 0:
                        first_item = data[0]
                        print(f"Sample keys: {list(first_item.keys())[:5]}")
                else:
                    print(f"Response type: {type(data)}")
            else:
                print(f"Error: {response.text[:100]}")
                
        except requests.exceptions.RequestException as e:
            print(f"\n{endpoint}")
            print(f"Connection Error: {str(e)}")
    
    # Test specific endpoints for map data
    print("\n=== Testing Map-Specific Endpoints ===")
    
    try:
        # Test heatmap data
        response = requests.get(f"{base_url}/monitoring/readings/heatmap_data/", timeout=5)
        print(f"\nHeatmap data endpoint:")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Heatmap points: {len(data)}")
            if len(data) > 0:
                print(f"Sample point: {data[0]}")
        
        # Test current zones
        response = requests.get(f"{base_url}/monitoring/zones/current_zones/", timeout=5)
        print(f"\nCurrent zones endpoint:")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Current zones: {len(data)}")
            if len(data) > 0:
                zone = data[0]
                print(f"Sample zone: {zone['name']} - {zone['zone_type']}")
                
    except requests.exceptions.RequestException as e:
        print(f"Connection Error: {str(e)}")

if __name__ == "__main__":
    test_api_endpoints()
