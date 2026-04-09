#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pollution_monitor.settings')
django.setup()

from monitoring.models import SensorReading

def check_data():
    print("Checking database...")
    try:
        count = SensorReading.objects.count()
        print(f"Total sensor readings: {count}")
        
        if count > 0:
            latest = SensorReading.objects.first()
            print(f"Latest reading: {latest.latitude}, {latest.longitude}, AQI: {latest.aqi}")
        
        # Test filtering
        from django.utils import timezone
        from datetime import timedelta
        
        recent = SensorReading.objects.filter(
            timestamp__gte=timezone.now() - timedelta(hours=1)
        ).count()
        print(f"Recent readings (last hour): {recent}")
        
        all_recent = SensorReading.objects.all()[:5]
        print(f"First 5 readings:")
        for reading in all_recent:
            print(f"  - AQI: {reading.aqi}, Location: {reading.latitude}, {reading.longitude}")
        
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    check_data()
