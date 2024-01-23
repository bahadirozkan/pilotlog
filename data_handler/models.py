from django.db import models

# Base abstract model for keeping guid
class BaseModel(models.Model):
    guid = models.CharField(max_length=255, primary_key=True) 

    class Meta:
        abstract = True

class Aircraft(BaseModel):
    Make = models.CharField(max_length=255, blank=True)
    Model = models.CharField(max_length=255, blank=True)
    Category = models.CharField(max_length=255, blank=True)
    Class = models.CharField(max_length=255, blank=True)
    EngType = models.CharField(max_length=255, verbose_name="EngineType", 
                               default="N/A")
    Complex = models.BooleanField()
    HighPerf = models.BooleanField(verbose_name="HighPerformance")

class Pilot(BaseModel):
    PilotName = models.CharField(max_length=255, verbose_name="Person1", 
                                 blank=True)
    PilotEMail = models.CharField(max_length=255, verbose_name="Person2", 
                                  blank=True)

class Airfield(BaseModel):
    AFName = models.CharField(max_length=255, verbose_name="Approach1")
    City = models.CharField(max_length=255, verbose_name="Approach2", 
                            blank=True)
    Notes = models.CharField(max_length=255, verbose_name="Approach3", 
                             blank=True)

class FlightManager(models.Manager):
    def merge_pilot_airfield_data(self):
        # Iterate over all Flight instances
        for flight in Flight.objects.all():
            guid = flight.guid

            try:
                # Try to get corresponding Airfield instance
                airfield_data = Airfield.objects.get(guid=guid)
                flight.airfield_data = airfield_data
            except Airfield.DoesNotExist:
                pass

            try:
                # Try to get corresponding Pilot instance
                pilot_data = Pilot.objects.get(guid=guid)
                flight.pilot_data = pilot_data
            except Pilot.DoesNotExist:
                pass

            flight.save()
        
        return flight
    
class Flight(BaseModel):
    DateLOCAL = models.CharField(max_length=255, verbose_name="Date")
    Route = models.CharField(max_length=255, blank=True)
    DepTimeUTC = models.CharField(max_length=255, verbose_name="TimeOut")
    ArrTimeUTC = models.CharField(max_length=255, verbose_name="TimeIn")
    minTOTAL = models.DecimalField(max_digits = 5, decimal_places = 2, 
                                   verbose_name="TotalTime")
    
    # One-to-one relationships with other models
    airfield_data = models.OneToOneField(Airfield, null=True, blank=True, 
                                         on_delete=models.CASCADE)
    pilot_data = models.OneToOneField(Pilot, null=True, blank=True, 
                                      on_delete=models.CASCADE)

    objects = FlightManager()

    class Meta:
        verbose_name_plural = "Flights"