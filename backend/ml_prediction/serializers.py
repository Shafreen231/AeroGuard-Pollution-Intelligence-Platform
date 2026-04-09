from rest_framework import serializers
from .models import PredictionModel, PollutionPrediction, ModelTrainingJob, PredictionAccuracy


class PredictionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionModel
        fields = '__all__'


class PollutionPredictionSerializer(serializers.ModelSerializer):
    pollution_level = serializers.CharField(source='get_pollution_level', read_only=True)
    model_name = serializers.CharField(source='model.name', read_only=True)
    
    class Meta:
        model = PollutionPrediction
        fields = '__all__'


class ModelTrainingJobSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source='model.name', read_only=True)
    
    class Meta:
        model = ModelTrainingJob
        fields = '__all__'


class PredictionAccuracySerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionAccuracy
        fields = '__all__'
