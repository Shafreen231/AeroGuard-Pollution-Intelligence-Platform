#!/usr/bin/env python
import requests
import json

def simple_test():
    try:
        print("Testing API...")
        response = requests.get("http://localhost:8000/api/monitoring/readings/latest/", timeout=10)
        print(f"Latest readings: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Received {len(data)} readings")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    simple_test()
