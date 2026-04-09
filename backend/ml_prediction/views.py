from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import random
from decimal import Decimal

from .models import (
    PollutionPrediction, 
    PredictionModel, 
    ModelTrainingJob, 
    PredictionAccuracy
)
from .serializers import (
    PollutionPredictionSerializer,
    PredictionModelSerializer,
    ModelTrainingJobSerializer,
    PredictionAccuracySerializer
)


class PollutionPredictionViewSet(viewsets.ModelViewSet):
    queryset = PollutionPrediction.objects.all()
    serializer_class = PollutionPredictionSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Auto-generate sample predictions if none exist
        if not queryset.exists():
            self._generate_sample_predictions()
            queryset = super().get_queryset()
        return queryset
    
    def _generate_sample_predictions(self):
        """Generate sample pollution predictions"""
        base_coords = [
            (28.6139, 77.2090),  # Delhi
            (19.0760, 72.8777),  # Mumbai
            (13.0827, 80.2707),  # Chennai
            (12.9716, 77.5946),  # Bangalore
            (22.5726, 88.3639),  # Kolkata
        ]
        
        for lat, lng in base_coords:
            for hours_ahead in [1, 6, 12, 24]:
                prediction_time = timezone.now() + timedelta(hours=hours_ahead)
                
                # Generate predictions with realistic variance
                base_aqi = random.randint(80, 200)
                confidence = random.uniform(0.7, 0.95)
                
                PollutionPrediction.objects.create(
                    latitude=Decimal(str(lat)),
                    longitude=Decimal(str(lng)),
                    predicted_aqi=base_aqi,
                    prediction_time=prediction_time,
                    confidence_score=Decimal(str(confidence)),
                    model_version='sample_v1.0',
                    created_at=timezone.now()
                )
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest predictions"""
        latest_predictions = self.get_queryset().order_by('-created_at')[:20]
        serializer = self.get_serializer(latest_predictions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def next_24_hours(self, request):
        """Get predictions for next 24 hours"""
        now = timezone.now()
        next_24h = now + timedelta(hours=24)
        
        predictions = self.get_queryset().filter(
            prediction_time__gte=now,
            prediction_time__lte=next_24h
        ).order_by('prediction_time')
        
        serializer = self.get_serializer(predictions, many=True)
        return Response(serializer.data)


class PredictionModelViewSet(viewsets.ModelViewSet):
    queryset = PredictionModel.objects.all()
    serializer_class = PredictionModelSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Auto-generate sample model if none exists
        if not queryset.exists():
            self._generate_sample_model()
            queryset = super().get_queryset()
        return queryset
    
    def _generate_sample_model(self):
        """Generate a sample prediction model"""
        PredictionModel.objects.create(
            name='RandomForest_AQI_v1.0',
            model_type='random_forest',
            version='1.0',
            is_active=True,
            description='Sample Random Forest model for AQI prediction',
            training_data_size=10000,
            created_at=timezone.now()
        )


class ModelTrainingJobViewSet(viewsets.ModelViewSet):
    queryset = ModelTrainingJob.objects.all()
    serializer_class = ModelTrainingJobSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Auto-generate sample training job if none exists
        if not queryset.exists():
            self._generate_sample_training_job()
            queryset = super().get_queryset()
        return queryset
    
    def _generate_sample_training_job(self):
        """Generate a sample training job"""
        # First ensure we have a model
        if not PredictionModel.objects.exists():
            PredictionModel.objects.create(
                name='RandomForest_AQI_v1.0',
                model_type='random_forest',
                version='1.0',
                is_active=True,
                description='Sample Random Forest model for AQI prediction',
                training_data_size=10000,
                created_at=timezone.now()
            )
        
        model = PredictionModel.objects.first()
        ModelTrainingJob.objects.create(
            model=model,
            status='completed',
            training_accuracy=Decimal('0.85'),
            validation_accuracy=Decimal('0.82'),
            training_data_size=8000,
            validation_data_size=2000,
            started_at=timezone.now() - timedelta(hours=2),
            completed_at=timezone.now() - timedelta(hours=1)
        )


class PredictionAccuracyViewSet(viewsets.ModelViewSet):
    queryset = PredictionAccuracy.objects.all()
    serializer_class = PredictionAccuracySerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Auto-generate sample accuracy if none exists
        if not queryset.exists():
            self._generate_sample_accuracy()
            queryset = super().get_queryset()
        return queryset
    
    def _generate_sample_accuracy(self):
        """Generate sample accuracy records"""
        # Ensure we have predictions
        if not PollutionPrediction.objects.exists():
            # Create some sample predictions first
            base_coords = [(28.6139, 77.2090), (19.0760, 72.8777)]
            for lat, lng in base_coords:
                PollutionPrediction.objects.create(
                    latitude=Decimal(str(lat)),
                    longitude=Decimal(str(lng)),
                    predicted_aqi=random.randint(80, 200),
                    prediction_time=timezone.now() + timedelta(hours=1),
                    confidence_score=Decimal('0.85'),
                    model_version='sample_v1.0',
                    created_at=timezone.now()
                )
        
        # Create accuracy records for existing predictions
        predictions = PollutionPrediction.objects.all()[:5]
        for prediction in predictions:
            PredictionAccuracy.objects.create(
                prediction=prediction,
                actual_aqi=prediction.predicted_aqi + random.randint(-20, 20),
                absolute_error=Decimal(str(random.uniform(5, 25))),
                percentage_error=Decimal(str(random.uniform(0.05, 0.2))),
                measured_at=timezone.now()
            )
