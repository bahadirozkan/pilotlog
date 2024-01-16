from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, AircraftViewSet, AircraftMetaViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'aircraft', AircraftViewSet)
router.register(r'aircraftmeta', AircraftMetaViewSet)

urlpatterns = [
    # api paths
    path('api/', include(router.urls)),
]
