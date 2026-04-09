from django.db import models
from django.utils import timezone


class Vehicle(models.Model):
    """Unmanned vehicles for pollution monitoring"""
    VEHICLE_TYPES = [
        ('drone', 'Drone'),
        ('ground_robot', 'Ground Robot'),
        ('boat', 'Boat'),
        ('stationary', 'Stationary Sensor'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
        ('malfunction', 'Malfunction'),
        ('offline', 'Offline'),
    ]
    
    vehicle_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Current location
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_altitude = models.FloatField(null=True, blank=True, help_text="Altitude in meters")
    
    # Technical specifications
    battery_level = models.IntegerField(default=100, help_text="Battery percentage")
    max_flight_time = models.IntegerField(help_text="Max flight time in minutes")
    max_range = models.FloatField(help_text="Max range in kilometers")
    sensor_capabilities = models.JSONField(default=list)  # List of sensors
    
    # Operational details
    last_communication = models.DateTimeField(null=True, blank=True)
    mission_status = models.CharField(max_length=50, default='standby')
    assigned_area = models.JSONField(null=True, blank=True)  # Polygon of assigned area
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.vehicle_id})"
    
    def is_online(self):
        """Check if vehicle is online based on last communication"""
        if not self.last_communication:
            return False
        return (timezone.now() - self.last_communication).seconds < 300  # 5 minutes
    
    def get_status_color(self):
        """Get color for status display"""
        colors = {
            'active': 'green',
            'inactive': 'gray',
            'maintenance': 'orange',
            'malfunction': 'red',
            'offline': 'black',
        }
        return colors.get(self.status, 'gray')


class VehicleMission(models.Model):
    """Missions assigned to vehicles"""
    MISSION_TYPES = [
        ('patrol', 'Area Patrol'),
        ('investigation', 'Pollution Investigation'),
        ('monitoring', 'Continuous Monitoring'),
        ('emergency', 'Emergency Response'),
    ]
    
    MISSION_STATUS = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    mission_type = models.CharField(max_length=20, choices=MISSION_TYPES)
    status = models.CharField(max_length=20, choices=MISSION_STATUS, default='pending')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], default='medium')
    
    # Mission area/waypoints
    waypoints = models.JSONField()  # List of coordinates
    estimated_duration = models.IntegerField(help_text="Estimated duration in minutes")
    
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.vehicle.name}"


class VehicleLocation(models.Model):
    """Track vehicle locations over time"""
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude = models.FloatField(null=True, blank=True)
    speed = models.FloatField(null=True, blank=True, help_text="Speed in m/s")
    heading = models.FloatField(null=True, blank=True, help_text="Heading in degrees")
    battery_level = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['vehicle', 'timestamp']),
            models.Index(fields=['latitude', 'longitude']),
        ]
    
    def __str__(self):
        return f"{self.vehicle.name} at ({self.latitude}, {self.longitude})"


class MaintenanceRecord(models.Model):
    """Maintenance records for vehicles"""
    MAINTENANCE_TYPES = [
        ('routine', 'Routine Maintenance'),
        ('repair', 'Repair'),
        ('calibration', 'Sensor Calibration'),
        ('upgrade', 'Hardware Upgrade'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPES)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    performed_by = models.CharField(max_length=100)
    parts_replaced = models.JSONField(default=list)
    
    scheduled_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.vehicle.name} - {self.get_maintenance_type_display()}"
