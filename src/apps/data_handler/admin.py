from django.contrib import admin

from .models import Aircraft, Airfield, Flight, Pilot


class BaseModelAdmin(admin.ModelAdmin):
    list_display = ('guid')

@admin.register(Aircraft)
class AircraftAdmin(BaseModelAdmin):
    list_display = ('guid', 'Make', 'Model', 'Category', 'Class',
                    'Complex', 'HighPerf')

@admin.register(Flight)
class FlightAdmin(BaseModelAdmin):
    list_display = ('guid', 'DateLOCAL', 'Route', 'DepTimeUTC',
                    'ArrTimeUTC', 'minTOTAL', 'pilot_data', 'airfield_data')

@admin.register(Pilot)
class PilotAdmin(BaseModelAdmin):
    list_display = ('guid', 'PilotName', 'PilotEMail')

@admin.register(Airfield)
class AirfieldAdmin(BaseModelAdmin):
    list_display = ('guid', 'AFName', 'City', 'Notes')
