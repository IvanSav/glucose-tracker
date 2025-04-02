from django.db import models


class Glucose(models.Model):
    user_id = models.UUIDField()
    timestamp = models.DateTimeField()
    record_type = models.IntegerField()
    glucose_value_trend = models.IntegerField(null=True, blank=True)
    glucose_scan = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Glucose Record ({self.user_id}) - {self.timestamp}"
