from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q, Avg
from datetime import timedelta
import requests
import random
from django.conf import settings

from .models import SensorReading, PollutionZone, PollutionAlert, ExternalAPIData
from .serializers import (
    SensorReadingSerializer, 
    PollutionZoneSerializer, 
    PollutionAlertSerializer,
    ExternalAPIDataSerializer
)


class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer
    
    def get_queryset(self):
        queryset = SensorReading.objects.all()
        
        # Auto-generate sample data if none exists
        if not queryset.exists():
            self._generate_sample_readings()
            queryset = SensorReading.objects.all()
        
        # Filter by time range
        hours = self.request.query_params.get('hours', None)
        if hours:
            since = timezone.now() - timedelta(hours=int(hours))
            queryset = queryset.filter(timestamp__gte=since)
        
        # Filter by location
        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)
        radius = self.request.query_params.get('radius', None)
        
        if lat and lng and radius:
            # Simple bounding box filter (for more accuracy, use geospatial queries)
            lat_range = float(radius) / 111.0  # Rough conversion
            lng_range = float(radius) / (111.0 * abs(float(lat)))
            
            queryset = queryset.filter(
                latitude__range=[float(lat) - lat_range, float(lat) + lat_range],
                longitude__range=[float(lng) - lng_range, float(lng) + lng_range]
            )
        
        return queryset
    
    def _generate_sample_readings(self):
        """Generate initial sample sensor readings"""
        # Sample coordinates around major Indian cities
        base_coords = [
            {'lat': 28.6139, 'lng': 77.2090, 'name': 'New Delhi'},
            {'lat': 19.0760, 'lng': 72.8777, 'name': 'Mumbai'},
            {'lat': 13.0827, 'lng': 80.2707, 'name': 'Chennai'},
            {'lat': 22.5726, 'lng': 88.3639, 'name': 'Kolkata'},
            {'lat': 12.9716, 'lng': 77.5946, 'name': 'Bangalore'},
        ]
        
        for coord in base_coords:
            # Generate readings in a small area around each coordinate
            for i in range(10):  # More readings for better map visualization
                lat_offset = random.uniform(-0.05, 0.05)
                lng_offset = random.uniform(-0.05, 0.05)
                
                # Generate realistic but random pollution data
                aqi = random.randint(50, 300)
                pm25 = random.uniform(20, 150)
                pm10 = random.uniform(30, 200)
                
                SensorReading.objects.create(
                    latitude=coord['lat'] + lat_offset,
                    longitude=coord['lng'] + lng_offset,
                    pm25=pm25,
                    pm10=pm10,
                    co=random.uniform(1, 15),
                    no2=random.uniform(20, 100),
                    so2=random.uniform(5, 50),
                    o3=random.uniform(80, 200),
                    aqi=aqi,
                    temperature=random.uniform(15, 35),
                    humidity=random.uniform(30, 80),
                    wind_speed=random.uniform(2, 20),
                    wind_direction=random.uniform(0, 360),
                    source='auto_generated',
                    is_real_time=False
                )
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest readings from all active vehicles"""
        latest_readings = SensorReading.objects.filter(
            timestamp__gte=timezone.now() - timedelta(hours=1)
        ).order_by('-timestamp')[:20]
        
        # If no readings exist, use all available readings
        if not latest_readings.exists():
            latest_readings = SensorReading.objects.all().order_by('-timestamp')[:20]
        
        serializer = self.get_serializer(latest_readings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def heatmap_data(self, request):
        """Get data for pollution heatmap"""
        hours = int(request.query_params.get('hours', 24))
        since = timezone.now() - timedelta(hours=hours)
        
        readings = SensorReading.objects.filter(
            timestamp__gte=since
        ).values('latitude', 'longitude', 'aqi', 'pm25', 'pm10')
        
        heatmap_data = []
        for reading in readings:
            heatmap_data.append({
                'lat': float(reading['latitude']),
                'lng': float(reading['longitude']),
                'aqi': reading['aqi'],
                'intensity': min(reading['aqi'] / 200.0, 1.0)  # Normalize for heatmap
            })
        
        return Response(heatmap_data)
    
    @action(detail=False, methods=['post'])
    def generate_sample_data(self, request):
        """Generate sample pollution data for testing"""
        # Sample coordinates around a city (you can modify these)
        base_coords = [
            {'lat': 28.6139, 'lng': 77.2090, 'name': 'New Delhi'},
            {'lat': 19.0760, 'lng': 72.8777, 'name': 'Mumbai'},
            {'lat': 13.0827, 'lng': 80.2707, 'name': 'Chennai'},
            {'lat': 22.5726, 'lng': 88.3639, 'name': 'Kolkata'},
            {'lat': 12.9716, 'lng': 77.5946, 'name': 'Bangalore'},
        ]
        
        created_readings = []
        
        for coord in base_coords:
            # Generate readings in a small area around each coordinate
            for i in range(5):
                lat_offset = random.uniform(-0.1, 0.1)
                lng_offset = random.uniform(-0.1, 0.1)
                
                # Generate realistic but random pollution data
                aqi = random.randint(50, 300)
                pm25 = random.uniform(20, 150)
                pm10 = random.uniform(30, 200)
                
                reading = SensorReading.objects.create(
                    latitude=coord['lat'] + lat_offset,
                    longitude=coord['lng'] + lng_offset,
                    pm25=pm25,
                    pm10=pm10,
                    co=random.uniform(1, 15),
                    no2=random.uniform(20, 100),
                    so2=random.uniform(5, 50),
                    o3=random.uniform(80, 200),
                    aqi=aqi,
                    temperature=random.uniform(15, 35),
                    humidity=random.uniform(30, 80),
                    wind_speed=random.uniform(2, 20),
                    wind_direction=random.uniform(0, 360),
                    source='sample_data',
                    is_real_time=False
                )
                created_readings.append(reading)
        
        serializer = self.get_serializer(created_readings, many=True)
        return Response({
            'message': f'Created {len(created_readings)} sample readings',
            'readings': serializer.data
        })


class PollutionZoneViewSet(viewsets.ModelViewSet):
    queryset = PollutionZone.objects.all()
    serializer_class = PollutionZoneSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Auto-generate sample zones if none exist
        if not queryset.exists():
            self._generate_sample_zones()
            queryset = super().get_queryset()
        return queryset
    
    def _generate_sample_zones(self):
        """Generate sample pollution zones for demonstration"""
        import random
        from decimal import Decimal
        
        # Major cities with realistic coordinates and pollution levels
        sample_zones = [
            {
                'name': 'Delhi Central',
                'zone_type': 'danger',
                'coordinates': {'lat': 28.6139, 'lng': 77.2090},
                'description': 'Delhi city center with high pollution',
                'aqi_threshold_min': 150,
                'aqi_threshold_max': 300
            },
            {
                'name': 'Mumbai South',
                'zone_type': 'moderate',
                'coordinates': {'lat': 19.0760, 'lng': 72.8777},
                'description': 'Mumbai downtown area',
                'aqi_threshold_min': 80,
                'aqi_threshold_max': 150
            },
            {
                'name': 'Chennai East',
                'zone_type': 'moderate',
                'coordinates': {'lat': 13.0827, 'lng': 80.2707},
                'description': 'Chennai coastal area',
                'aqi_threshold_min': 70,
                'aqi_threshold_max': 120
            },
            {
                'name': 'Bangalore IT Hub',
                'zone_type': 'safe',
                'coordinates': {'lat': 12.9716, 'lng': 77.5946},
                'description': 'Bangalore technology corridor',
                'aqi_threshold_min': 30,
                'aqi_threshold_max': 80
            },
            {
                'name': 'Kolkata Industrial',
                'zone_type': 'danger',
                'coordinates': {'lat': 22.5726, 'lng': 88.3639},
                'description': 'Kolkata industrial zone',
                'aqi_threshold_min': 120,
                'aqi_threshold_max': 250
            }
        ]
        
        for zone_data in sample_zones:
            PollutionZone.objects.create(**zone_data)
    
    @action(detail=False, methods=['get'])
    def current_zones(self, request):
        """Get current pollution zones with real-time data"""
        zones = self.get_queryset()
        zone_data = []
        
        for zone in zones:
            # Get recent readings in this zone (simplified check)
            recent_readings = SensorReading.objects.filter(
                timestamp__gte=timezone.now() - timedelta(hours=1)
            ).aggregate(avg_aqi=Avg('aqi'))
            
            zone_info = self.get_serializer(zone).data
            zone_info['current_aqi'] = recent_readings['avg_aqi'] or 0
            zone_data.append(zone_info)
        
        return Response(zone_data)


class PollutionAlertViewSet(viewsets.ModelViewSet):
    queryset = PollutionAlert.objects.filter(is_active=True)
    serializer_class = PollutionAlertSerializer
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Mark an alert as resolved"""
        alert = self.get_object()
        alert.is_active = False
        alert.resolved_at = timezone.now()
        alert.save()
        
        return Response({'message': 'Alert resolved successfully'})


class ExternalAPIDataViewSet(viewsets.ModelViewSet):
    queryset = ExternalAPIData.objects.all()
    serializer_class = ExternalAPIDataSerializer
    
    @action(detail=False, methods=['post'])
    def fetch_openweather_data(self, request):
        """Fetch pollution data from OpenWeatherMap API"""
        lat = request.data.get('lat')
        lng = request.data.get('lng')
        city_name = request.data.get('city_name', 'Unknown')
        
        if not lat or not lng:
            return Response(
                {'error': 'Latitude and longitude are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        api_key = getattr(settings, 'OPENWEATHERMAP_API_KEY', 'your_api_key_here')
        if api_key == 'your_api_key_here':
            # Generate mock data if no API key is configured
            mock_data = {
                'coord': {'lon': float(lng), 'lat': float(lat)},
                'list': [{
                    'main': {'aqi': random.randint(1, 5)},
                    'components': {
                        'co': random.uniform(200, 1000),
                        'no': random.uniform(0, 50),
                        'no2': random.uniform(20, 100),
                        'o3': random.uniform(80, 200),
                        'so2': random.uniform(5, 50),
                        'pm2_5': random.uniform(20, 150),
                        'pm10': random.uniform(30, 200),
                        'nh3': random.uniform(0, 20)
                    }
                }]
            }
            
            # Save mock data
            api_data = ExternalAPIData.objects.create(
                api_source='openweathermap_mock',
                location_name=city_name,
                latitude=lat,
                longitude=lng,
                raw_data=mock_data
            )
            
            # Create sensor reading from mock data
            components = mock_data['list'][0]['components']
            SensorReading.objects.create(
                latitude=lat,
                longitude=lng,
                pm25=components['pm2_5'],
                pm10=components['pm10'],
                co=components['co'] / 1000,  # Convert to mg/m³
                no2=components['no2'],
                so2=components['so2'],
                o3=components['o3'],
                aqi=mock_data['list'][0]['main']['aqi'] * 50,  # Convert to US AQI scale
                temperature=random.uniform(15, 35),
                humidity=random.uniform(30, 80),
                wind_speed=random.uniform(2, 20),
                wind_direction=random.uniform(0, 360),
                source='openweathermap_mock',
                is_real_time=True
            )
            
            return Response({
                'message': 'Mock data generated successfully',
                'data': self.get_serializer(api_data).data
            })
        
        return Response({'message': 'OpenWeatherMap integration ready'})
