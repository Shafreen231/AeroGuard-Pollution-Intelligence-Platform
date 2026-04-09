from rest_framework import serializers
from .models import Vehicle, VehicleMission, VehicleLocation, MaintenanceRecord


class VehicleSerializer(serializers.ModelSerializer):
    status_color = serializers.CharField(source='get_status_color', read_only=True)
    is_online = serializers.BooleanField(read_only=True)
    last_reading_time = serializers.DateTimeField(source='last_communication', read_only=True)
    
    class Meta:
        model = Vehicle
        fields = '__all__'


class VehicleMissionSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.CharField(source='vehicle.name', read_only=True)
    
    class Meta:
        model = VehicleMission
        fields = '__all__'


class VehicleLocationSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.CharField(source='vehicle.name', read_only=True)
    
    class Meta:
        model = VehicleLocation
        fields = '__all__'


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.CharField(source='vehicle.name', read_only=True)
    
    class Meta:
        model = MaintenanceRecord
        fields = '__all__'
