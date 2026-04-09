#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pollution_monitor.settings')
django.setup()

from monitoring.views import SensorReadingViewSet
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import AnonymousUser

def test_viewset():
    print("Testing SensorReadingViewSet...")
    
    try:
        # Create a request factory
        factory = APIRequestFactory()
        request = factory.get('/api/monitoring/readings/latest/')
        request.user = AnonymousUser()
        
        # Create viewset instance
        viewset = SensorReadingViewSet()
        viewset.request = request
        viewset.format_kwarg = None
        
        # Test the latest action
        response = viewset.latest(request)
        print(f"Response status: {response.status_code}")
        print(f"Response data length: {len(response.data)}")
        
        if len(response.data) > 0:
            print(f"First item keys: {list(response.data[0].keys())}")
            print(f"Sample reading: AQI={response.data[0].get('aqi')}, lat={response.data[0].get('latitude')}")
        
        return True
        
    except Exception as e:
        print(f"Error in viewset: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_viewset()
