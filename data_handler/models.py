from django.db import models

class UserManager(models.Manager):
    pass

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)

    objects = UserManager()

    def __str__(self):
        return f"User {self.user_id}"

class AircraftQuerySet(models.QuerySet):
    pass

class AircraftManager(models.Manager):
    def get_queryset(self):
        return AircraftQuerySet(self.model, using=self._db)

    def aircraft_for_user(self, user_id):
        return self.get_queryset().filter(user__user_id=user_id)

class Aircraft(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.CharField(max_length=255)
    guid = models.UUIDField(primary_key=True)
    platform = models.IntegerField()
    _modified = models.IntegerField()

    objects = AircraftManager()

    def __str__(self):
        return f"{self.guid} - {self.table}"

class AircraftMeta(models.Model):
    aircraft = models.OneToOneField(Aircraft, on_delete=models.CASCADE, primary_key=True)
    fin = models.CharField(max_length=255)
    sea = models.BooleanField()
    tmg = models.BooleanField()
    efis = models.BooleanField()
    # Add other fields

    def __str__(self):
        return f"Meta for Aircraft: {self.aircraft.guid}"

