from django.db import models


class BaseModel(models.Model):
    """# Base abstract model for keeping guid"""
    guid = models.CharField(max_length=255, primary_key=True)

    class Meta:
        abstract = True

class Aircraft(BaseModel):
    """Aircraft model that inherits from BaseModel"""
    Make = models.CharField(max_length=255, blank=True)
    Model = models.CharField(max_length=255, blank=True)
    Category = models.CharField(max_length=255, blank=True)
    Class = models.CharField(max_length=255, blank=True)
    EngType = models.CharField(max_length=255, verbose_name="EngineType",
                               default="N/A")
    Complex = models.BooleanField()
    HighPerf = models.BooleanField(verbose_name="HighPerformance")

class Pilot(BaseModel):
    """Pilot model that inherits from BaseModel"""
    PilotName = models.CharField(max_length=255, verbose_name="Person1",
                                 blank=True)
    PilotEMail = models.CharField(max_length=255, verbose_name="Person2",
                                  blank=True)

class Airfield(BaseModel):
    """Airfield model that inherits from BaseModel"""
    AFName = models.CharField(max_length=255, verbose_name="Approach1")
    City = models.CharField(max_length=255, verbose_name="Approach2",
                            blank=True)
    Notes = models.CharField(max_length=255, verbose_name="Approach3",
                             blank=True)

class FlightManager(models.Manager):
    """
    Manager model to contain merge_pilot_airfield_data function
    """
    def merge_pilot_airfield_data(self) -> bool:
        """
        Merges Flight, Pilot and Airfield data on ID (guid)
        Instances of Airfield and Pilot is much less than Flight.
        For that reason first the instances of Airfield and Pilot are
        retrieved and those ids are updated on Flight to merge.

        Return True is not strictly required. It's for testing.
        """

        # Retrieve all unique guids from Pilot and Airfield
        all_guids = set(Pilot.objects.values_list('guid', flat=True)) | \
                    set(Airfield.objects.values_list('guid', flat=True))

        # Update Flight instances in bulk
        for guid in all_guids:
            try:
                pilot_data = Pilot.objects.get(guid=guid)
            except Pilot.DoesNotExist:
                pilot_data = None

            try:
                airfield_data = Airfield.objects.get(guid=guid)
            except Airfield.DoesNotExist:
                airfield_data = None

            Flight.objects.filter(guid=guid).update(
                pilot_data=pilot_data,
                airfield_data=airfield_data
            )

        return True

class Flight(BaseModel):
    """
    Airfield model that inherits from BaseModel. Contains Flight Manager
    to merge Flight data with Airfield and Pilot data.
    """
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
