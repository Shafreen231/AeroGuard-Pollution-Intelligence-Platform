from django.db import models
from django.utils import timezone


class PollutionZone(models.Model):
    """Pollution zones with safety levels"""
    ZONE_TYPES = [
        ('safe', 'Safe (Green)'),
        ('moderate', 'Moderate (Orange)'),
        ('danger', 'Danger (Red)'),
    ]
    
    name = models.CharField(max_length=100)
    zone_type = models.CharField(max_length=10, choices=ZONE_TYPES)
    coordinates = models.JSONField()  # Store polygon coordinates
    description = models.TextField(blank=True)
    aqi_threshold_min = models.IntegerField()
    aqi_threshold_max = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_zone_type_display()})"


class SensorReading(models.Model):
    """Individual sensor readings from vehicles or external sources"""
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Pollution parameters
    pm25 = models.FloatField(help_text="PM2.5 concentration (μg/m³)")
    pm10 = models.FloatField(help_text="PM10 concentration (μg/m³)")
    co = models.FloatField(help_text="Carbon Monoxide (mg/m³)")
    no2 = models.FloatField(help_text="Nitrogen Dioxide (μg/m³)")
    so2 = models.FloatField(help_text="Sulfur Dioxide (μg/m³)")
    o3 = models.FloatField(help_text="Ozone (μg/m³)")
    aqi = models.IntegerField(help_text="Air Quality Index")
    
    # Environmental parameters
    temperature = models.FloatField(help_text="Temperature (°C)")
    humidity = models.FloatField(help_text="Humidity (%)")
    wind_speed = models.FloatField(help_text="Wind Speed (m/s)")
    wind_direction = models.FloatField(help_text="Wind Direction (degrees)")
    
    timestamp = models.DateTimeField(default=timezone.now)
    is_real_time = models.BooleanField(default=True)
    source = models.CharField(max_length=50, default='vehicle')  # vehicle, api, manual
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['aqi']),
        ]
    
    def __str__(self):
        return f"Reading at ({self.latitude}, {self.longitude}) - AQI: {self.aqi}"
    
    def get_pollution_level(self):
        """Determine pollution level based on AQI"""
        if self.aqi <= 50:
            return 'safe'
        elif self.aqi <= 100:
            return 'moderate'
        else:
            return 'danger'


class PollutionAlert(models.Model):
    """Alerts for dangerous pollution levels"""
    ALERT_TYPES = [
        ('high_aqi', 'High AQI'),
        ('rapid_increase', 'Rapid Increase'),
        ('vehicle_malfunction', 'Vehicle Sensor Malfunction'),
        ('zone_threshold', 'Zone Threshold Exceeded'),
    ]
    
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    message = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    severity = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.severity}"


class ExternalAPIData(models.Model):
    """Store data from external APIs like OpenWeatherMap"""
    api_source = models.CharField(max_length=50)
    location_name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    raw_data = models.JSONField()
    processed_data = models.JSONField(null=True, blank=True)
    fetched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fetched_at']
    
    def __str__(self):
        return f"{self.api_source} - {self.location_name}"
