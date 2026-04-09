from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from decimal import Decimal
from monitoring.models import SensorReading, PollutionZone
from vehicles.models import Vehicle
from ml_prediction.models import PollutionPrediction


class Command(BaseCommand):
    help = 'Generate sample data for pollution monitoring system'

    def handle(self, *args, **options):
        self.stdout.write('Generating sample data...')
        
        # Generate sensor readings
        self.generate_sensor_readings()
        
        # Generate pollution zones
        self.generate_pollution_zones()
        
        # Generate vehicles
        self.generate_vehicles()
        
        # Generate predictions
        self.generate_predictions()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully generated sample data!')
        )

    def generate_sensor_readings(self):
        """Generate sample sensor readings"""
        if SensorReading.objects.exists():
            self.stdout.write('Sensor readings already exist. Skipping...')
            return
            
        base_coords = [
            {'lat': 28.6139, 'lng': 77.2090, 'name': 'New Delhi'},
            {'lat': 19.0760, 'lng': 72.8777, 'name': 'Mumbai'},
            {'lat': 13.0827, 'lng': 80.2707, 'name': 'Chennai'},
            {'lat': 22.5726, 'lng': 88.3639, 'name': 'Kolkata'},
            {'lat': 12.9716, 'lng': 77.5946, 'name': 'Bangalore'},
        ]
        
        count = 0
        for coord in base_coords:
            for i in range(10):
                lat_offset = random.uniform(-0.05, 0.05)
                lng_offset = random.uniform(-0.05, 0.05)
                
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
                    source='sample_data',
                    is_real_time=False
                )
                count += 1
        
        self.stdout.write(f'Generated {count} sensor readings')

    def generate_pollution_zones(self):
        """Generate sample pollution zones"""
        if PollutionZone.objects.exists():
            self.stdout.write('Pollution zones already exist. Skipping...')
            return
            
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
        
        count = 0
        for zone_data in sample_zones:
            PollutionZone.objects.create(**zone_data)
            count += 1
        
        self.stdout.write(f'Generated {count} pollution zones')

    def generate_vehicles(self):
        """Generate sample vehicles"""
        if Vehicle.objects.exists():
            self.stdout.write('Vehicles already exist. Skipping...')
            return
            
        vehicle_types = ['drone', 'ground_robot', 'boat']
        statuses = ['active', 'maintenance', 'inactive']
        
        base_coords = [
            (28.6139, 77.2090),  # Delhi
            (19.0760, 72.8777),  # Mumbai
            (13.0827, 80.2707),  # Chennai
            (12.9716, 77.5946),  # Bangalore
            (22.5726, 88.3639),  # Kolkata
        ]
        
        count = 0
        for i, (lat, lng) in enumerate(base_coords):
            for j in range(2):  # 2 vehicles per city
                vehicle_type = random.choice(vehicle_types)
                status = random.choice(statuses)
                
                Vehicle.objects.create(
                    vehicle_id=f'VEH_{i+1:02d}_{j+1:02d}',
                    name=f'{vehicle_type.title()} {i+1}-{j+1}',
                    vehicle_type=vehicle_type,
                    status=status,
                    current_latitude=Decimal(str(lat + random.uniform(-0.01, 0.01))),
                    current_longitude=Decimal(str(lng + random.uniform(-0.01, 0.01))),
                    battery_level=random.randint(20, 100),
                    max_flight_time=random.randint(30, 120),
                    max_range=random.uniform(5.0, 25.0),
                    sensor_capabilities=['PM2.5', 'PM10', 'NO2', 'CO'],
                    last_communication=timezone.now() - timedelta(minutes=random.randint(1, 60)),
                    mission_status='patrol'
                )
                count += 1
        
        self.stdout.write(f'Generated {count} vehicles')

    def generate_predictions(self):
        """Generate sample predictions"""
        if PollutionPrediction.objects.exists():
            self.stdout.write('Predictions already exist. Skipping...')
            return
            
        from ml_prediction.models import PredictionModel
        
        # First ensure we have a prediction model
        if not PredictionModel.objects.exists():
            model = PredictionModel.objects.create(
                name='Sample Random Forest v1.0',
                model_type='random_forest',
                description='Sample Random Forest model for demonstration',
                is_active=True,
                is_trained=True,
                training_data_count=5000,
                accuracy_score=0.85,
                mae=15.2,
                rmse=22.8,
                r2_score=0.82
            )
        else:
            model = PredictionModel.objects.first()
            
        base_coords = [
            (28.6139, 77.2090),  # Delhi
            (19.0760, 72.8777),  # Mumbai
            (13.0827, 80.2707),  # Chennai
            (12.9716, 77.5946),  # Bangalore
            (22.5726, 88.3639),  # Kolkata
        ]
        
        count = 0
        for lat, lng in base_coords:
            for hours_ahead in [1, 6, 12, 24]:
                prediction_date = timezone.now() + timedelta(hours=hours_ahead)
                
                # Generate predictions with realistic variance
                base_aqi = random.randint(80, 200)
                confidence = random.uniform(0.7, 0.95)
                
                PollutionPrediction.objects.create(
                    model=model,
                    latitude=Decimal(str(lat)),
                    longitude=Decimal(str(lng)),
                    prediction_for_date=prediction_date,
                    prediction_horizon=hours_ahead,
                    predicted_aqi=base_aqi,
                    predicted_pm25=random.uniform(20, 100),
                    predicted_pm10=random.uniform(30, 150),
                    predicted_co=random.uniform(1, 10),
                    predicted_no2=random.uniform(20, 80),
                    predicted_so2=random.uniform(5, 40),
                    predicted_o3=random.uniform(80, 160),
                    confidence_score=confidence,
                    uncertainty_range={'aqi': [base_aqi-10, base_aqi+10]},
                    input_features={'temperature': 25, 'humidity': 60, 'wind_speed': 5},
                    weather_features={'temp': 25, 'humidity': 60}
                )
                count += 1
        
        self.stdout.write(f'Generated {count} predictions')
