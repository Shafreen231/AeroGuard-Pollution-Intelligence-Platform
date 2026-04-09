from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'models', views.PredictionModelViewSet)
router.register(r'predictions', views.PollutionPredictionViewSet)
router.register(r'training-jobs', views.ModelTrainingJobViewSet)
router.register(r'accuracy', views.PredictionAccuracyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
