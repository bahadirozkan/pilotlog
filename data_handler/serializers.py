from rest_framework import serializers
from .models import User, Aircraft, AircraftMeta

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AircraftMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftMeta
        fields = '__all__'

class AircraftSerializer(serializers.ModelSerializer):
    aircraftmeta = AircraftMetaSerializer()

    class Meta:
        model = Aircraft
        fields = '__all__'
