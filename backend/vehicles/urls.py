from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'vehicles', views.VehicleViewSet)
router.register(r'missions', views.VehicleMissionViewSet)
router.register(r'locations', views.VehicleLocationViewSet)
router.register(r'maintenance', views.MaintenanceRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
