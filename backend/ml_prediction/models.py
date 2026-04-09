from django.db import models
from django.utils import timezone


class PredictionModel(models.Model):
    """ML model configurations for pollution prediction"""
    MODEL_TYPES = [
        ('linear_regression', 'Linear Regression'),
        ('random_forest', 'Random Forest'),
        ('neural_network', 'Neural Network'),
        ('arima', 'ARIMA'),
    ]
    
    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    description = models.TextField()
    
    # Model parameters
    parameters = models.JSONField(default=dict)
    features_used = models.JSONField(default=list)  # List of features used for training
    target_variable = models.CharField(max_length=50, default='aqi')
    
    # Model performance metrics
    accuracy_score = models.FloatField(null=True, blank=True)
    mae = models.FloatField(null=True, blank=True, help_text="Mean Absolute Error")
    rmse = models.FloatField(null=True, blank=True, help_text="Root Mean Square Error")
    r2_score = models.FloatField(null=True, blank=True, help_text="R-squared Score")
    
    # Model status
    is_active = models.BooleanField(default=False)
    is_trained = models.BooleanField(default=False)
    training_data_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_trained = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_model_type_display()})"


class PollutionPrediction(models.Model):
    """Pollution predictions for specific locations and times"""
    model = models.ForeignKey(PredictionModel, on_delete=models.CASCADE)
    
    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    location_name = models.CharField(max_length=100, blank=True)
    
    # Prediction details
    prediction_for_date = models.DateTimeField()
    prediction_horizon = models.IntegerField(help_text="Hours ahead")
    
    # Predicted values
    predicted_aqi = models.FloatField()
    predicted_pm25 = models.FloatField()
    predicted_pm10 = models.FloatField()
    predicted_co = models.FloatField()
    predicted_no2 = models.FloatField()
    predicted_so2 = models.FloatField()
    predicted_o3 = models.FloatField()
    
    # Confidence and uncertainty
    confidence_score = models.FloatField(help_text="Confidence in prediction (0-1)")
    uncertainty_range = models.JSONField(default=dict)  # Min/max ranges for each parameter
    
    # Input features used
    input_features = models.JSONField()
    weather_features = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-prediction_for_date']
        indexes = [
            models.Index(fields=['prediction_for_date']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['predicted_aqi']),
        ]
    
    def __str__(self):
        return f"Prediction for {self.prediction_for_date} - AQI: {self.predicted_aqi}"
    
    def get_pollution_level(self):
        """Determine pollution level based on predicted AQI"""
        if self.predicted_aqi <= 50:
            return 'safe'
        elif self.predicted_aqi <= 100:
            return 'moderate'
        else:
            return 'danger'


class ModelTrainingJob(models.Model):
    """Track model training jobs"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    model = models.ForeignKey(PredictionModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Training configuration
    training_start_date = models.DateTimeField()
    training_end_date = models.DateTimeField()
    data_sources = models.JSONField(default=list)  # Sources of training data
    
    # Results
    training_samples = models.IntegerField(null=True, blank=True)
    validation_samples = models.IntegerField(null=True, blank=True)
    training_metrics = models.JSONField(default=dict)
    validation_metrics = models.JSONField(default=dict)
    
    # Execution details
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    logs = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Training {self.model.name} - {self.status}"


class PredictionAccuracy(models.Model):
    """Track accuracy of predictions vs actual measurements"""
    prediction = models.OneToOneField(PollutionPrediction, on_delete=models.CASCADE)
    actual_aqi = models.FloatField(null=True, blank=True)
    actual_pm25 = models.FloatField(null=True, blank=True)
    actual_pm10 = models.FloatField(null=True, blank=True)
    actual_co = models.FloatField(null=True, blank=True)
    actual_no2 = models.FloatField(null=True, blank=True)
    actual_so2 = models.FloatField(null=True, blank=True)
    actual_o3 = models.FloatField(null=True, blank=True)
    
    # Error metrics
    aqi_error = models.FloatField(null=True, blank=True)
    pm25_error = models.FloatField(null=True, blank=True)
    pm10_error = models.FloatField(null=True, blank=True)
    
    measured_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-measured_at']
    
    def __str__(self):
        return f"Accuracy for {self.prediction}"
    
    def calculate_errors(self):
        """Calculate prediction errors"""
        if self.actual_aqi and self.prediction.predicted_aqi:
            self.aqi_error = abs(self.actual_aqi - self.prediction.predicted_aqi)
        if self.actual_pm25 and self.prediction.predicted_pm25:
            self.pm25_error = abs(self.actual_pm25 - self.prediction.predicted_pm25)
        if self.actual_pm10 and self.prediction.predicted_pm10:
            self.pm10_error = abs(self.actual_pm10 - self.prediction.predicted_pm10)
