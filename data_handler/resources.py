from import_export import resources
from .models import User, Aircraft, AircraftMeta

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class AircraftResource(resources.ModelResource):
    class Meta:
        model = Aircraft

class AircraftMetaResource(resources.ModelResource):
    class Meta:
        model = AircraftMeta
