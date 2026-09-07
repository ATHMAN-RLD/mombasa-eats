from django.db import models
from accounts.models import Rider


class RiderLocation(models.Model):
    rider = models.OneToOneField(Rider, on_delete=models.CASCADE, related_name="location")
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rider} @ ({self.latitude}, {self.longitude})"  