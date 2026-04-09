from rest_framework import serializers
from .models import SensorReading, PollutionZone, PollutionAlert, ExternalAPIData


class SensorReadingSerializer(serializers.ModelSerializer):
    pollution_level = serializers.CharField(source='get_pollution_level', read_only=True)
    vehicle_name = serializers.CharField(source='vehicle.name', read_only=True)
    
    class Meta:
        model = SensorReading
        fields = '__all__'


class PollutionZoneSerializer(serializers.ModelSerializer):
    center_latitude = serializers.SerializerMethodField()
    center_longitude = serializers.SerializerMethodField()
    pollution_level = serializers.CharField(source='zone_type', read_only=True)
    radius = serializers.SerializerMethodField()
    last_updated = serializers.CharField(source='updated_at', read_only=True)
    
    class Meta:
        model = PollutionZone
        fields = ['id', 'name', 'center_latitude', 'center_longitude', 'radius', 
                 'pollution_level', 'description', 'last_updated']
    
    def get_center_latitude(self, obj):
        if isinstance(obj.coordinates, dict):
            return obj.coordinates.get('lat', 0)
        return 28.6139  # Default to Delhi center
    
    def get_center_longitude(self, obj):
        if isinstance(obj.coordinates, dict):
            return obj.coordinates.get('lng', 0)
        return 77.2090  # Default to Delhi center
    
    def get_radius(self, obj):
        # Return a default radius in meters for the circle
        return 5000  # 5km radius


class PollutionAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollutionAlert
        fields = '__all__'


class ExternalAPIDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalAPIData
        fields = '__all__'
