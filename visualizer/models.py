from django.db import models

class Batch(models.Model):
    # Model to store batch meta data
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.DurationField()
    batch_id = models.CharField(max_length=10)

class SensorData(models.Model):
    # Model to store sensor data
    timestamp = models.DateTimeField()
    value = models.FloatField()
    sensor = models.CharField(max_length=10)


