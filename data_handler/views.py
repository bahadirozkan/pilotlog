from rest_framework import viewsets
from .models import User, Aircraft, AircraftMeta
from .serializers import UserSerializer, AircraftSerializer, AircraftMetaSerializer
from django.contrib import admin
from import_export.admin import ImportExportMixin
from .resources import UserResource, AircraftResource, AircraftMetaResource


class UserImportExportView(ImportExportMixin, admin.ModelAdmin):
    resource_class = UserResource


class AircraftImportExportView(ImportExportMixin, admin.ModelAdmin):
    resource_class = AircraftResource


class AircraftMetaImportExportView(ImportExportMixin, admin.ModelAdmin):
    resource_class = AircraftMetaResource


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer


class AircraftMetaViewSet(viewsets.ModelViewSet):
    queryset = AircraftMeta.objects.all()
    serializer_class = AircraftMetaSerializer
