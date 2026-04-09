from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'readings', views.SensorReadingViewSet)
router.register(r'zones', views.PollutionZoneViewSet)
router.register(r'alerts', views.PollutionAlertViewSet)
router.register(r'external-data', views.ExternalAPIDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
