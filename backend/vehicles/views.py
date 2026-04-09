from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import random

from .models import Vehicle, VehicleMission, VehicleLocation, MaintenanceRecord
from .serializers import (
    VehicleSerializer, 
    VehicleMissionSerializer, 
    VehicleLocationSerializer,
    MaintenanceRecordSerializer
)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    
    def get_queryset(self):
        # Generate sample vehicles if none exist
        if not Vehicle.objects.exists():
            self._generate_sample_vehicles()
        return Vehicle.objects.all()
    
    def _generate_sample_vehicles(self):
        """Generate sample vehicles for testing"""
        vehicle_types = ['drone', 'ground_robot', 'boat']
        statuses = ['active', 'inactive', 'maintenance', 'charging']
        
        # Sample coordinates around major cities
        locations = [
            {'lat': 28.6139, 'lng': 77.2090, 'name': 'Delhi'},
            {'lat': 19.0760, 'lng': 72.8777, 'name': 'Mumbai'},
            {'lat': 13.0827, 'lng': 80.2707, 'name': 'Chennai'},
            {'lat': 22.5726, 'lng': 88.3639, 'name': 'Kolkata'},
            {'lat': 12.9716, 'lng': 77.5946, 'name': 'Bangalore'},
        ]
        
        for i, location in enumerate(locations):
            for j in range(2):  # 2 vehicles per location
                vehicle_type = random.choice(vehicle_types)
                status = random.choice(statuses)
                
                # Create slight position variations
                lat_offset = random.uniform(-0.01, 0.01)
                lng_offset = random.uniform(-0.01, 0.01)
                
                Vehicle.objects.create(
                    name=f"{location['name']} {vehicle_type.title()} {j+1}",
                    vehicle_type=vehicle_type,
                    current_latitude=location['lat'] + lat_offset,
                    current_longitude=location['lng'] + lng_offset,
                    battery_level=random.randint(20, 100),
                    status=status,
                    last_active=timezone.now() - timedelta(minutes=random.randint(0, 120))
                )
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active vehicles"""
        active_vehicles = Vehicle.objects.filter(status='active')
        serializer = self.get_serializer(active_vehicles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def map_data(self, request):
        """Get vehicle data for map display"""
        vehicles = Vehicle.objects.filter(
            current_latitude__isnull=False,
            current_longitude__isnull=False
        )
        
        map_data = []
        for vehicle in vehicles:
            map_data.append({
                'id': vehicle.id,
                'name': vehicle.name,
                'vehicle_id': vehicle.vehicle_id,
                'type': vehicle.vehicle_type,
                'status': vehicle.status,
                'lat': float(vehicle.current_latitude),
                'lng': float(vehicle.current_longitude),
                'battery_level': vehicle.battery_level,
                'last_communication': vehicle.last_communication,
                'is_online': vehicle.is_online(),
                'status_color': vehicle.get_status_color()
            })
        
        return Response(map_data)
    
    @action(detail=True, methods=['post'])
    def update_location(self, request, pk=None):
        """Update vehicle location"""
        vehicle = self.get_object()
        lat = request.data.get('latitude')
        lng = request.data.get('longitude')
        altitude = request.data.get('altitude')
        battery = request.data.get('battery_level')
        
        if lat and lng:
            vehicle.current_latitude = lat
            vehicle.current_longitude = lng
            vehicle.current_altitude = altitude
            if battery:
                vehicle.battery_level = battery
            vehicle.last_communication = timezone.now()
            vehicle.save()
            
            # Create location record
            VehicleLocation.objects.create(
                vehicle=vehicle,
                latitude=lat,
                longitude=lng,
                altitude=altitude,
                battery_level=battery or vehicle.battery_level
            )
            
            return Response({'message': 'Location updated successfully'})
        
        return Response(
            {'error': 'Latitude and longitude are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['post'])
    def create_sample_vehicles(self, request):
        """Create sample vehicles for testing"""
        sample_vehicles = [
            {
                'vehicle_id': 'DRONE001',
                'name': 'Environmental Drone Alpha',
                'vehicle_type': 'drone',
                'current_latitude': 28.6139,
                'current_longitude': 77.2090,
                'battery_level': random.randint(60, 100),
                'max_flight_time': 45,
                'max_range': 15.0,
                'sensor_capabilities': ['PM2.5', 'PM10', 'CO', 'NO2', 'SO2', 'O3', 'Temperature', 'Humidity']
            },
            {
                'vehicle_id': 'ROBOT001',
                'name': 'Ground Monitor Beta',
                'vehicle_type': 'ground_robot',
                'current_latitude': 19.0760,
                'current_longitude': 72.8777,
                'battery_level': random.randint(60, 100),
                'max_flight_time': 480,  # 8 hours
                'max_range': 50.0,
                'sensor_capabilities': ['PM2.5', 'PM10', 'CO', 'NO2', 'Noise Level']
            },
            {
                'vehicle_id': 'STATION001',
                'name': 'Central Monitoring Station',
                'vehicle_type': 'stationary',
                'current_latitude': 13.0827,
                'current_longitude': 80.2707,
                'battery_level': 100,
                'max_flight_time': 0,
                'max_range': 0,
                'sensor_capabilities': ['PM2.5', 'PM10', 'CO', 'NO2', 'SO2', 'O3', 'Temperature', 'Humidity', 'Wind Speed']
            }
        ]
        
        created_vehicles = []
        for vehicle_data in sample_vehicles:
            vehicle, created = Vehicle.objects.get_or_create(
                vehicle_id=vehicle_data['vehicle_id'],
                defaults=vehicle_data
            )
            if created:
                created_vehicles.append(vehicle)
        
        serializer = self.get_serializer(created_vehicles, many=True)
        return Response({
            'message': f'Created {len(created_vehicles)} sample vehicles',
            'vehicles': serializer.data
        })


class VehicleMissionViewSet(viewsets.ModelViewSet):
    queryset = VehicleMission.objects.all()
    serializer_class = VehicleMissionSerializer
    
    @action(detail=False, methods=['get'])
    def active_missions(self, request):
        """Get all active missions"""
        active_missions = VehicleMission.objects.filter(
            status__in=['pending', 'in_progress']
        )
        serializer = self.get_serializer(active_missions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def start_mission(self, request, pk=None):
        """Start a mission"""
        mission = self.get_object()
        if mission.status == 'pending':
            mission.status = 'in_progress'
            mission.started_at = timezone.now()
            mission.save()
            
            # Update vehicle status
            mission.vehicle.mission_status = f"Mission: {mission.title}"
            mission.vehicle.save()
            
            return Response({'message': 'Mission started successfully'})
        
        return Response(
            {'error': 'Mission cannot be started'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class VehicleLocationViewSet(viewsets.ModelViewSet):
    queryset = VehicleLocation.objects.all()
    serializer_class = VehicleLocationSerializer
    
    def get_queryset(self):
        queryset = VehicleLocation.objects.all()
        vehicle_id = self.request.query_params.get('vehicle_id', None)
        if vehicle_id:
            queryset = queryset.filter(vehicle__id=vehicle_id)
        
        hours = self.request.query_params.get('hours', None)
        if hours:
            since = timezone.now() - timedelta(hours=int(hours))
            queryset = queryset.filter(timestamp__gte=since)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def tracking_data(self, request):
        """Get tracking data for all vehicles"""
        vehicle_id = request.query_params.get('vehicle_id')
        hours = int(request.query_params.get('hours', 24))
        since = timezone.now() - timedelta(hours=hours)
        
        if vehicle_id:
            locations = VehicleLocation.objects.filter(
                vehicle__id=vehicle_id,
                timestamp__gte=since
            ).order_by('timestamp')
        else:
            # Get latest location for each vehicle
            locations = VehicleLocation.objects.filter(
                timestamp__gte=since
            ).order_by('vehicle', '-timestamp').distinct('vehicle')
        
        tracking_data = []
        for location in locations:
            tracking_data.append({
                'vehicle_id': location.vehicle.id,
                'vehicle_name': location.vehicle.name,
                'lat': float(location.latitude),
                'lng': float(location.longitude),
                'altitude': location.altitude,
                'battery_level': location.battery_level,
                'timestamp': location.timestamp,
                'speed': location.speed,
                'heading': location.heading
            })
        
        return Response(tracking_data)


class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecord.objects.all()
    serializer_class = MaintenanceRecordSerializer
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming maintenance"""
        upcoming = MaintenanceRecord.objects.filter(
            is_completed=False,
            scheduled_date__gte=timezone.now()
        ).order_by('scheduled_date')
        
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue maintenance"""
        overdue = MaintenanceRecord.objects.filter(
            is_completed=False,
            scheduled_date__lt=timezone.now()
        ).order_by('scheduled_date')
        
        serializer = self.get_serializer(overdue, many=True)
        return Response(serializer.data)
